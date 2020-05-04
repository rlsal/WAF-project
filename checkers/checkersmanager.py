from threading import Lock
import checkers.implementations
import importlib
import inspect
from alert import Alert
from config import Config

_checkers = None
_load_lock = Lock()


def _load():
    global _checkers

    if _checkers is None:
        _load_lock.acquire()
        try:
            if _checkers is None:
                _checkers = []
                for module_name in checkers.implementations.__all__:
                    module = importlib.import_module('checkers.implementations.%s' % module_name)

                    for member in inspect.getmembers(module):
                        if inspect.isclass(member[1]) and \
                           member[0] != 'BaseChecker' and \
                           member[0].endswith('Checker'):
                            checker = member[1]()
                            if not checker.is_enabled():
                                continue

                            # Registering the just-instantiated checker
                            _checkers.append(checker)
        finally:
            _load_lock.release()


def check_request(data, context):
    return _check(data, context, lambda checker, data, context: checker.check_request(data, context))


def check_response(data, context):
    return _check(data, context, lambda checker, data, context: checker.check_response(data, context))


def _check(data, context, check_function):
    # Ensure checkers registration
    _load()

    is_valid = True
    for checker in _checkers:
        processed_data = check_function(checker, data, context)
        if processed_data is not None:
            data = processed_data
        else:
            attack_config = Config.get_attack_config(checker.get_attack_name())
            if attack_config is None:
                continue

            if attack_config['action'] == 'ids':
                Alert.add_alert(alert_type=attack_config['report_type'],
                                action_taken='LOGGED',
                                event='Attack %s was found' % checker.get_attack_name())
            elif attack_config['action'] == 'ips':
                Alert.add_alert(alert_type=attack_config['report_type'],
                                action_taken='ABORTED',
                                event='Attack %s was found' % checker.get_attack_name())
                is_valid = False

    return data if is_valid else None
