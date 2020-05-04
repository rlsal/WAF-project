from checkers.basechecker import BaseChecker
import re


class UsingKnownVulnerableComponentsChecker(BaseChecker):
    VULNERABILITIES = {
        'Server': {
            'Microsoft-IIS/7.5': ['CVE-2012-2531', 'CVE-2010-3972'],
            'Microsoft-IIS/7.0': ['CVE-2008-1446'],
            'Microsoft-IIS/6.0': ['CVE-2009-3023', 'CVE-2008-1446'],
            'nginx/1.9.9': ['CVE-2016-0742', 'CVE-2016-0746', 'CVE-2016-0747']
        },
        'X-Powered-By': {
            'PHP/5.5.34': ['CVE-2016-4539'],
            'PHP/5.6.0': ['CVE-2016-4539', 'CVE-2016-3141'],
            'PHP/5.6.1': ['CVE-2016-4539', 'CVE-2016-3141'],
            'PHP/5.6.2': ['CVE-2016-4539', 'CVE-2016-3141'],
            'PHP/5.6.3': ['CVE-2016-4539', 'CVE-2016-3141'],
            'PHP/5.6.4': ['CVE-2016-4539', 'CVE-2016-3141'],
            'PHP/7.0.1': ['CVE-2015-8617']
        }
    }

    def get_attack_name(self):
        return 'using_known_vulnerable_components'

    def is_enabled(self):
        return True

    def check_request(self, request, context):
        return request

    def check_response(self, response, context):
        for header_name in UsingKnownVulnerableComponentsChecker.VULNERABILITIES.keys():
            header_value_matches = re.search(re.compile('.*%s: ([^\r\n]+)\r\n' % header_name), response)
            if header_value_matches and \
               header_value_matches.groups()[0] in UsingKnownVulnerableComponentsChecker.VULNERABILITIES[header_name]:
                return None

        return response
