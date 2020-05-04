from checkers.basechecker import BaseChecker
from handlers.basehandler import BaseHandler
import re


class CsrfChecker(BaseChecker):
    CSRF_HEADER_NAME = 'X-CSRF-Token'
    CSRF_PARAM_NAME = 'csrftoken'

    def get_attack_name(self):
        return 'csrf'

    def is_enabled(self):
        return True

    def check_request(self, request, context):
        if not request.startswith('POST'):
            return request

        header_matches = re.search('\r\n%s: ([^\r\n]+)\r\n' % CsrfChecker.CSRF_HEADER_NAME, request)
        if header_matches and header_matches.groups()[0] in BaseHandler.session_ids:
            return request

        param_matches = re.search('%s=([^=&]+)' % CsrfChecker.CSRF_PARAM_NAME, request)
        if param_matches and param_matches.groups()[0] in BaseHandler.session_ids:
            return request

        return None

    def check_response(self, response, context):
        if 'session_data' not in context:
            return response

        return re.sub('(<form\s+[^>]*method\s*=\s*(\'|")\s*post\s*(\'|")[^>]*>)',
                      r'\1<input type="hidden" name="%s" value="%s" />' % (CsrfChecker.CSRF_PARAM_NAME,
                                                                           context['session_data']['id']),
                      response, flags=re.IGNORECASE)
