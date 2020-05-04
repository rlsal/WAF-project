import re
import urllib

from checkers.basechecker import BaseChecker
from HTMLParser import HTMLParser


class XssChecker(BaseChecker):
    def get_attack_name(self):
        return 'xss'

    def is_enabled(self):
        return True

    def check_request(self, request, context):
        h = HTMLParser()
        unescaped_trimmed_request = urllib.unquote(h.unescape(request.replace(' ', '').replace('\\n','').lower()))
        xss_attacks_matches = [
            re.search('<script', unescaped_trimmed_request),
            re.search('src=', unescaped_trimmed_request),
            re.search('javascript:', unescaped_trimmed_request),
            re.search('xss', unescaped_trimmed_request),
            re.search('<div', unescaped_trimmed_request),
            re.search('<style', unescaped_trimmed_request),
            re.search('<href', unescaped_trimmed_request),
            re.search('<body', unescaped_trimmed_request),
            re.search('<!--', unescaped_trimmed_request),
            re.search('attr([\s]*)=', unescaped_trimmed_request),
            re.search('<img=', unescaped_trimmed_request),
            re.search('<iframe=', unescaped_trimmed_request),
            re.search('<input=', unescaped_trimmed_request),
            re.search('dynsrc([\s]*)=', unescaped_trimmed_request),
            re.search('lowsrc([\s]*)=', unescaped_trimmed_request),
            re.search('fscommand()', unescaped_trimmed_request),
            re.search('on.+\(\)', unescaped_trimmed_request), # Covers "on" javascript functions
        ]

        if any([xss_regex_match is not None and xss_regex_match.group(0) is not None
                for xss_regex_match in xss_attacks_matches]):
            return None
        else:
            return request

    def check_response(self, response, context):
        return response
