import json
import datetime


class Alert:
    @staticmethod
    def get_alerts():
        with open('alerts.json', 'r') as alerts_file:
            alerts = json.load(alerts_file)

        return alerts

    @staticmethod
    def add_alert(alert_type='INFO', timestamp=None, event=None, action_taken=None, attacker_ip=None):
        alerts = [{
            'alert_type': alert_type,
            'timestamp': (timestamp or datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
            'event': event,
            'action_taken': action_taken,
            'attacker_ip': attacker_ip
        }]
        alerts += Alert.get_alerts()

        with open('alerts.json', 'w') as alerts_file:
            alerts_file.write(json.dumps(alerts))
            alerts_file.flush()
