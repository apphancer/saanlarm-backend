from flask import Flask, request, jsonify
from control_state import control_state, set_led_colours
from alarm_checker import check_alarm
from user_settings import load_user_settings, save_user_settings, get_led_state, set_led_state, get_alarm_time, set_alarm_time
from threading import Thread
import config  # Import the config module

app = Flask(__name__)

# Load user settings at startup
load_user_settings()

def periodic_alarm_check():
    """
    Periodically checks the alarm condition.
    """
    global running
    while running:
        if led_state['state'] == "alarm" and alarm_time:
            check_alarm(led_state['state'], alarm_time)
        time.sleep(60)  # Check every minute (adjust as needed)

@app.route('/led-state', methods=['GET'])
def get_led_state_endpoint():
    return jsonify(get_led_state())

@app.route('/led-state', methods=['POST'])
def set_led_state_endpoint():
    data = request.get_json()
    return set_led_state(data)

@app.route('/alarm-time', methods=['GET'])
def get_alarm_endpoint():
    return jsonify(get_alarm_time())

@app.route('/alarm-time', methods=['POST'])
def set_alarm_endpoint():
    data = request.get_json()
    return set_alarm_time(data)

@app.route('/colours', methods=['POST'])
def set_colours():
    data = request.get_json()
    # your set_colour logic
    return jsonify({"message": "Colours updated"}), 200

if __name__ == '__main__':
    # Start the background thread for periodic checks
    alarm_thread = Thread(target=periodic_alarm_check)
    alarm_thread.daemon = True  # Allows thread to exit when main program exits
    alarm_thread.start()
    app.run(host=config.HOST, port=config.PORT)