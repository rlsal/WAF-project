from checkers.basechecker import BaseChecker
import re


class SecurityMisconfigurationChecker(BaseChecker):
    def get_attack_name(self):
        return 'security_misconfiguration'

    def is_enabled(self):
        return True

    def check_request(self, request, context):
        return request

    def check_response(self, response, context):
        status_code = response.split()[1]
        is_server_error = re.match('5[\d][\d]', status_code) is not None
        return response if not is_server_error else None
