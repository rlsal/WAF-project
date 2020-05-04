from checkers.basechecker import BaseChecker
import re


class InsecureDirectObjectReferencesChecker(BaseChecker):
    FORBIDDEN_PATTERNS = [
        # Following expression covers the different forms of the '../' and '..\' traversal paths:
        # - Normal: '../'
        # - Encoded:
        #   - '%2e./'
        #   - '.%2e/'
        #   - '..%2f'
        #   - '%2e%2e/'
        #   - '%2e.%2f'
        #   - '.%2e%2f'
        # - Double Encoded:
        #   - '%2e%2e%2f'
        #   - etc.
        '(\.|%2e|%252e){2}(\\\\|/|%2f|%252f|%5c|%255c)',

        # Absolute *NIX traversal paths
        '/var/.*',
        '/etc/.*/',
        '/bin/.*',
        '/sbin/.*',
        '/lib(64)?/.*',
        '/dev/.*/',
        '/mnt/.*',
        '/opt/.*',
        '/tmp/.*',

        # Absolute Windows traversal paths
        '[A-Za-z]:(\\\\|/)[^\\\\|/]+'
    ]

    def get_attack_name(self):
        return 'insecure_direct_object_references'

    def is_enabled(self):
        return True

    def check_request(self, request, context):
        for pattern in InsecureDirectObjectReferencesChecker.FORBIDDEN_PATTERNS:
            if re.search(pattern, request, flags=re.IGNORECASE) is not None:
                return None

        return request

    def check_response(self, response, context):
        return response
