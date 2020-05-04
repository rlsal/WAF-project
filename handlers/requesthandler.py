from config import Config, Setting
import logging
import re
import base64
import os

from basehandler import BaseHandler
from checkers import checkersmanager

SUPPORTED_HTTP_METHODS = ['GET', 'POST', 'PUT']
IMPLICIT_PROTOCOLS = [80]
SESSION_ID_BYTES_LENGTH = 60


class RequestHandler(BaseHandler):
    def __init__(self, proxy_server):
        super(RequestHandler, self).__init__(proxy_server=proxy_server)

    def handle(self, inbound_socket, forward_socket, data, context):
        # Data format validation (RFC 2616)
        request_matches = \
            re.search('^(GET|POST|PUT) ([^ ]+) (HTTP/[0-9\.]+)\r\n([A-Za-z\-]+: [^\r\n]+\r\n)*($|\r\n.*)', data)
        if request_matches is None:
            return None

        session_id_matches = re.search('Cookie: [^\r\n]*%s=([^; \r\n]+)' % BaseHandler.SESSION_ID_COOKIE_NAME, data)
        if session_id_matches is None:
            context['session_data'] = {
                'id': base64.urlsafe_b64encode(os.urandom(SESSION_ID_BYTES_LENGTH)),
                'fresh': True
            }
        else:
            context['session_data'] = {
                'id': session_id_matches.groups()[0],
                'fresh': False
            }

        request_method = request_matches.groups()[0]
        request_path = request_matches.groups()[1]

        if request_method not in SUPPORTED_HTTP_METHODS:
            return None

        # Prohibited file types validation
        file_type_matches = re.match('([^\.]*\.([^/\?]*))', request_path)
        if file_type_matches is not None:
            requested_file_type = file_type_matches.groups()[1]
            for prohibited_file_type in Config.get_setting(Setting.PROHIBITED_FILE_TYPES).split(','):
                if requested_file_type == prohibited_file_type:
                    return None

        processed_data = checkersmanager.check_request(data, context)
        if processed_data is None:
            return None

        logging.info('Forwarding %s request to %s' % (request_method, request_path))

        # Replace the host header before transmitting
        processed_data = processed_data.replace(
            'Host: %s%s' % (
                self.proxy_server.listen_address[0], ':' + str(self.proxy_server.listen_address[1])
                if self.proxy_server.listen_address[1] not in IMPLICIT_PROTOCOLS
                else ''),
            'Host: %s%s' % (
                self.proxy_server.remote_address[0], ':' + str(self.proxy_server.remote_address[1])
                if self.proxy_server.remote_address[1] not in IMPLICIT_PROTOCOLS
                else ''))
        return processed_data
