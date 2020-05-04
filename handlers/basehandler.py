import abc


class BaseHandler(object):
    __metaclass__ = abc.ABCMeta

    # Fireharry Session ID Cookie
    SESSION_ID_COOKIE_NAME = 'FHSID'

    session_ids = {}

    def __init__(self, proxy_server=None):
        self.proxy_server = proxy_server

    @abc.abstractmethod
    def handle(self, inbound_socket, forward_socket, data, context):
        """Handles the proxied data and returns True if the data was forwarded, False otherwise"""
