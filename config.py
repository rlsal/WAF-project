import json
from alert import Alert


class Setting(object):
    SYSTEM_MODE = 'system_mode'
    PROHIBITED_FILE_TYPES = 'prohibited_file_types'


class Config:
    @staticmethod
    def get_config():
        config_json = None
        with open('config.json', 'r') as config_file:
            config_json = json.load(config_file)

        return config_json

    @staticmethod
    def save_config(config_json):

        # we do this to make sure that the json is valid
        validated_config_json = json.loads(config_json)
        with open('config.json', 'w') as config_file:
            config_file.write(json.dumps(validated_config_json))
            config_file.flush()

    @staticmethod
    def get_setting(setting_name):
        config_json = Config.get_config()
        return config_json.get(setting_name)

    @staticmethod
    def get_attack_config(attack_name):
        config_json = Config.get_config()
        if not config_json.get(Setting.SYSTEM_MODE):
            Alert.add_alert(alert_type='ERROR', event='Could not find \'system_mode\' on config.json')
            return None
        elif config_json[Setting.SYSTEM_MODE] == 'no_action':
            return None
        elif config_json[Setting.SYSTEM_MODE] != 'per_attack':
            return {'action': config_json['system_mode'], 'report_type': 'WARN'}
        elif not config_json.get('attack_types'):
            Alert.add_alert(alert_type='ERROR', event='Could not find \'attack_types\' on config.json')
            return None
        else:
            for attack_type in config_json['attack_types']:
                if attack_type.get('name') == attack_name:
                    if not attack_type.get('per_attack_action'):
                        Alert.add_alert(
                            alert_type='ERROR',
                            event='No \'per_attack_action\' found for \'%s\' on config.json' % attack_name)
                    elif not attack_type.get('report_type'):
                        Alert.add_alert(
                            alert_type='ERROR',
                            event='No \'report_type\' found for \'%s\' on config.json' % attack_name)
                    elif attack_type['per_attack_action'] == 'no_action':
                        return None
                    else:
                        return {'action': attack_type['per_attack_action'], 'report_type': attack_type['report_type']}

            Alert.add_alert(
                alert_type='ERROR',
                event='Could not find attack \'%s\' on config.json' % attack_name)

            return None
