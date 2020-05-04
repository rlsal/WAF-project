import json

import flask
from flask import Flask, request
from config import Config
from alert import Alert
from cors import crossdomain

application = app = Flask(__name__)
app.debug = True


# Routes
@app.route('/config', methods=['GET', 'OPTIONS'])
def get_config():
    if request.method is 'OPTIONS':
        return True

    config = Config.get_config()

    return json.dumps(config)


@app.route('/config', methods=['POST', 'OPTIONS'])
def set_config():
    if request.method is 'OPTIONS':
        return True

    config_json = request.data

    if config_json is not None:
        Config.save_config(config_json)

    return json.dumps(True)


@app.route('/alerts', methods=['GET'])
def get_alerts():
    alerts = Alert.get_alerts()

    rows = [[alert['timestamp'],
             alert['alert_type'],
             alert['event'],
             alert['action_taken'],
             alert['attacker_ip']]
            for alert in alerts]

    return json.dumps({
        'data': rows
    })
