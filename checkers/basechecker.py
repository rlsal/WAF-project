import abc


class BaseChecker(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_attack_name(self):
        """Returns the name of the attack (also used to identify it in the configuration file)"""

    @abc.abstractmethod
    def is_enabled(self):
        """Returns True if the checker is currently enabled, False otherwise"""

    @abc.abstractmethod
    def check_request(self, request, context):
        """Returns the request (possibly modified) if the checker considered the request to be valid,
        None otherwise"""

    @abc.abstractmethod
    def check_response(self, response, context):
        """Returns the response (possibly modified) if the checker considered the response to be valid,
        None otherwise"""
