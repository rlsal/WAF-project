from basehandler import BaseHandler
from checkers import checkersmanager
from datetime import datetime
import re


class ResponseHandler(BaseHandler):
    def __init__(self, proxy_server):
        super(ResponseHandler, self).__init__(proxy_server=proxy_server)

    def handle(self, inbound_socket, forward_socket, data, context):
        response_parts = data.split()
        if not response_parts[0].startswith('HTTP'):
            return data

        # Data format validation (RFC 2616)
        response_matches = \
            re.search('^(HTTP/[0-9\.]+) (\d{3}) [A-Za-z\- ]+\r\n([A-Za-z\-]+: [^\r\n]+\r\n)*', data)
        if response_matches is None:
            return None

        if 'session_data' in context and context['session_data']['fresh'] is True:
            data = data.replace('\r\n', '\r\nSet-Cookie: %s=%s; Path=/\r\n' %
                                (BaseHandler.SESSION_ID_COOKIE_NAME, context['session_data']['id']), 1)
            BaseHandler.session_ids[context['session_data']['id']] = datetime.now()
            context['session_data']['fresh'] = False

        processed_data = checkersmanager.check_response(data, context)
        if processed_data is None:
            return None

        return processed_data
