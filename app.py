from flask import Flask, request, jsonify
from alarm_checker import check_alarm
from user_settings import (
    load_user_settings, save_user_settings, get_alarm_time, set_alarm_time, get_rgbw_values, set_rgbw_values
)
from threading import Thread
import config
import time
from rotary import start_rotary_thread
from datetime import timedelta

app = Flask(__name__)

# Load user settings at startup
load_user_settings()

alarm_triggered = False  # Flag to ensure the alarm starts only once


def fade_in_led():
    duration_seconds = 5 * 60  # 5 minutes
    steps = 255
    step_duration = duration_seconds / steps

    for brightness in range(steps):
        rgbw_data = {"red": 0, "green": 0, "blue": 0, "white": brightness}
        response, status_code = set_rgbw_values(rgbw_data)
        time.sleep(step_duration)  # wait for the next step


def periodic_alarm_check():
    global running, alarm_triggered
    running = True

    while running:
        alarm_info = get_alarm_time()
        alarm_time = alarm_info['alarm_time']
        alarm_state = alarm_info['alarm_state']

        # Perform the alarm check
        if alarm_state == "enabled" and alarm_time:
            result = check_alarm(alarm_state, alarm_time)
            if result == "ALARM STARTING" and not alarm_triggered:
                print(result)  # Print ALARM STARTING only once
                alarm_triggered = True
                fade_in_led()  # Start fading in the LED brightness
            elif result != "ALARM STARTING":
                alarm_triggered = False  # Reset the flag if not in the alarm window
        time.sleep(60)

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