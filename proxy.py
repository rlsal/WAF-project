from handlers import requesthandler, responsehandler, httperrors
from trafficdirection import TrafficDirection
import socket
import select
import time
import sys
import argparse
from alert import Alert
import logging
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from threading import Thread
import rest_api

BUFFER_SIZE = 4096
MAX_CONNECTIONS = 1024
POLLING_DELAY = 0.01
SERVER_THREADS_DELAY = 1
RECEIVE_TIMEOUT = 0.1
RECEIVE_DELAY = 0.01


class ProxyServer:
    def __init__(self, listen_host, listen_port, remote_host, remote_port):
        self.sockets = []
        self.channels = {}

        self.listen_address = (listen_host, listen_port)
        self.remote_address = (remote_host, remote_port)

        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.main_socket.bind(self.listen_address)
        self.main_socket.listen(MAX_CONNECTIONS)

        self.request_handler = requesthandler.RequestHandler(self)
        self.response_handler = responsehandler.ResponseHandler(self)

    def start(self):
        self.sockets.append(self.main_socket)
        while True:
            time.sleep(POLLING_DELAY)

            # Asking the OS to determine the sockets that have data that's ready and waiting to be processed
            input_ready, output_ready, except_ready = select.select(self.sockets, [], [])
            for ready_socket in input_ready:
                if ready_socket == self.main_socket:
                    self.accept_incoming_connection()
                    break

                try:
                    data = ProxyServer.receive_socket_data(ready_socket)
                    if len(data) == 0:
                        self.close_connection(ready_socket)
                        break
                    else:
                        self.handle_incoming_data(ready_socket, data)
                # In case the connection was unexpectedly reset by peer, close it
                except socket.error:
                    self.close_connection(ready_socket)
                    break

    def accept_incoming_connection(self):
        forwarding_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        forwarding_socket.connect(self.remote_address)

        client_socket, client_address = self.main_socket.accept()
        if forwarding_socket:
            Alert.add_alert(event='New Connection: %s, %s' % client_address)
            context = {}
            self.sockets.append(client_socket)
            self.sockets.append(forwarding_socket)
            self.channels[client_socket] = {
                'socket': forwarding_socket,
                'direction': TrafficDirection.inbound,
                'context': context
            }
            self.channels[forwarding_socket] = {
                'socket': client_socket,
                'direction': TrafficDirection.outbound,
                'context': context
            }
        else:
            Alert.add_alert(alert_type='WARN', event='Proxy could not connect to remote, closing client connection')
            client_socket.close()

    def close_connection(self, ready_socket):
        paired_socket = self.channels[ready_socket]['socket']

        # Remove objects from sockets list
        self.sockets.remove(ready_socket)
        self.sockets.remove(paired_socket)

        # Remove the channel mappings
        del self.channels[ready_socket]
        del self.channels[paired_socket]

        # Close the connections
        ready_socket.close()
        paired_socket.close()

    def handle_incoming_data(self, ready_socket, data):
        if self.channels[ready_socket]['direction'] == TrafficDirection.inbound:
            inbound_socket = ready_socket
            outbound_socket = self.channels[ready_socket]['socket']
            handle_function = self.request_handler.handle
            context = self.channels[ready_socket]['context']
        else:
            inbound_socket = self.channels[ready_socket]['socket']
            outbound_socket = ready_socket
            handle_function = self.response_handler.handle
            context = self.channels[ready_socket]['context']

        processed_data = handle_function(inbound_socket, outbound_socket, data, context)
        if processed_data is not None:
            # In case the relevant handler found the data valid, forward it to the other socket on the channel
            self.channels[ready_socket]['socket'].send(processed_data)
        else:
            # Otherwise, return an error page and terminate the connection
            inbound_socket.send(httperrors.FORBIDDEN_RESPONSE)
            self.close_connection(ready_socket)

    @staticmethod
    def receive_socket_data(ready_socket, timeout=RECEIVE_TIMEOUT):
        ready_socket.setblocking(0)
        data_parts = []

        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                break

            try:
                data = ready_socket.recv(BUFFER_SIZE)
                if data:
                    data_parts.append(data)
                    start_time = time.time()
                else:
                    time.sleep(RECEIVE_DELAY)
            except socket.error:
                pass

        return ''.join(data_parts)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Proxy Server')
    parser.add_argument('remote_host', type=str)
    parser.add_argument('--remote_port', type=int, default=80)
    parser.add_argument('--listen_host', type=str, default='localhost')
    parser.add_argument('--listen_port', type=int, default=8080)
    parser.add_argument('--management-port', type=int, default=5000)
    args = parser.parse_args()

    server_threads = []
    try:
        # Preparing proxy thread
        event = '[PROXY] Starting to listen on %s:%s' % (args.listen_host, args.listen_port)
        logging.info(event)
        Alert.add_alert(event=event)

        server = ProxyServer(args.listen_host, args.listen_port, args.remote_host, args.remote_port)
        server_threads.append(Thread(target=server.start))

        # Preparing management thread
        event = '[MANAGEMENT] Starting to listen on localhost:%s' % args.management_port
        logging.info(event)
        Alert.add_alert(event=event)

        http_server = HTTPServer(WSGIContainer(rest_api.app))
        http_server.listen(args.management_port)
        management_server = IOLoop.instance()
        server_threads.append(Thread(target=management_server.start))

        # Starting allx threads
        for thread in server_threads:
            thread.daemon = True
            thread.start()

        logging.info('Servers started (CTRL+C to stop)')
        while True:
            time.sleep(SERVER_THREADS_DELAY)

    except KeyboardInterrupt:
        event = 'Closing server'
        logging.info(event)
        Alert.add_alert(event=event)

        # Stopping threads
        for thread in server_threads:
            thread.join(0)

        sys.exit(1)
