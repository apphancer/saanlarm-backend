from flask import Flask, request, jsonify
from alarm_checker import check_alarm, fade_in_led, stop_alarm, fade_in_running
from user_settings import (
    load_user_settings, save_user_settings, get_alarm_time, set_alarm_time, get_rgbw_values, set_rgbw_values, get_alarm_state, set_alarm_state
)
from threading import Thread
import config
import time
from rotary import start_rotary_thread

app = Flask(__name__)

# Load user settings at startup
load_user_settings()

alarm_triggered = False  # Flag to ensure the alarm starts only once

# can this be moved to alarm_checker.py?
def periodic_alarm_check():
    global running, alarm_triggered, fade_in_running
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
                if not fade_in_running:
                    fade_in_led(fade_in_completed)
            elif result != "ALARM STARTING":
                alarm_triggered = False  # Reset the flag if not in the alarm window
                if fade_in_running:
                    fade_in_running = False
                    print("ALARM STOPPED")
        time.sleep(60)

# can this be moved to alarm_checker.py?
def fade_in_completed():
    global fade_in_running
    fade_in_running = False
    print("ALARM STOPPED")

@app.route('/alarm', methods=['GET'])
def get_alarm_endpoint():
    return jsonify(get_alarm_time())

@app.route('/alarm', methods['POST'])
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