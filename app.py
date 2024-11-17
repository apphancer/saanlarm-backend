from flask import Flask, request, jsonify
from control_state import control_state
from alarm_checker import check_alarm
from user_settings import (
    load_user_settings, save_user_settings, get_state,
    set_state, get_alarm_time, set_alarm_time, get_rgbw_values, set_rgbw_values
)
from threading import Thread
import config
import time
from rotary import start_rotary_thread

app = Flask(__name__)

load_user_settings()

def periodic_alarm_check():
    global running
    running = True

    while running:
        if get_state()['state'] == "alarm" and alarm_time:
            check_alarm(get_state()['state'], alarm_time)
        time.sleep(60)

@app.route('/state', methods=['GET'])
def get_state_endpoint():
    return jsonify(get_state())

@app.route('/state', methods=['POST'])
def set_state_endpoint():
    data = request.get_json()
    return set_state(data)

@app.route('/alarm-time', methods=['GET'])
def get_alarm_endpoint():
    return jsonify(get_alarm_time())

@app.route('/alarm-time', methods=['POST'])
def set_alarm_endpoint():
    data = request.get_json()
    return set_alarm_time(data)

@app.route('/colours', methods=['GET'])
def get_colours():
    return jsonify(get_rgbw_values()), 200

@app.route('/colours', methods=['POST'])
def set_colours():
    data = request.get_json()
    response, status_code = set_rgbw_values(data)
    return jsonify(response), status_code

if __name__ == '__main__':
    start_rotary_thread()
    alarm_thread = Thread(target=periodic_alarm_check)
    alarm_thread.daemon = True
    alarm_thread.start()
    app.run(host=config.HOST, port=config.PORT)