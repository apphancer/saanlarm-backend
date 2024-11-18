from flask import Flask, request, jsonify
from alarm_checker import periodic_alarm_check, fade_in_completed
from user_settings import (
    load_user_settings, save_user_settings, get_alarm_time, set_alarm_time, get_rgbw_values, set_rgbw_values, get_alarm_state, set_alarm_state
)
from threading import Thread
import config
from rotary import start_rotary_thread

app = Flask(__name__)

# Load user settings at startup
load_user_settings()

fade_in_running = False
alarm_triggered = False

@app.route('/alarm', methods=['GET'])
def get_alarm_endpoint():
    return jsonify(get_alarm_time())

@app.route('/alarm', methods=['POST'])
def set_alarm_endpoint():
    data = request.get_json()
    response, status_code = set_alarm_time(data)
    return jsonify(response), status_code

@app.route('/colours', methods=['GET'])
def get_colours():
    return jsonify(get_rgbw_values()), 200

@app.route('/colours', methods['POST'])
def set_colours():
    data = request.get_json()
    response, status_code = set_rgbw_values(data)
    return jsonify(response), status_code

if __name__ == '__main__':
    start_rotary_thread()
    alarm_thread = Thread(target=periodic_alarm_check, args=(alarm_triggered, fade_in_running))
    alarm_thread.daemon = True
    alarm_thread.start()
    app.run(host=config.HOST, port=config.PORT)