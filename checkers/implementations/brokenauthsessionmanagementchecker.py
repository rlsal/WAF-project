from checkers.basechecker import BaseChecker
import re


class BrokenAuthenticationAndSessionManagementChecker(BaseChecker):
    KNOWN_SESSION_ID_URL_PATTERNS = ['.*sessionid=', 'phpsessid=']

    def get_attack_name(self):
        return 'broken_auth'

    def is_enabled(self):
        return True

    def check_request(self, request, context):
        path = request.split(' ')[1]

        if path is not None and any([re.search(pattern, path.lower()) is not None
                                    for pattern
                                    in BrokenAuthenticationAndSessionManagementChecker.KNOWN_SESSION_ID_URL_PATTERNS]):
            return None

        return request

    def check_response(self, response, context):
        return response
