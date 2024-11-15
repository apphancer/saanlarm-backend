from flask import Flask, request, jsonify
from control_state import control_state, set_led_colours
from alarm_checker import check_alarm
from user_settings import (
    load_user_settings, save_user_settings, get_led_state,
    set_led_state, get_alarm_time, set_alarm_time, rgbw_values
)
from threading import Thread
from led import set_led_colours
import config

app = Flask(__name__)

load_user_settings()

def periodic_alarm_check():
    """
    Periodically checks the alarm condition.
    """
    global running
    while running:
        if led_state['state'] == "alarm" and alarm_time:
            check_alarm(led_state['state'], alarm_time)
        time.sleep(60)


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

@app.route('/colours', methods=['GET'])
def get_colours():
    """
    Endpoint to get the current RGBW values.
    """
    return jsonify(rgbw_values), 200  # Return current rgbw_values

@app.route('/colours', methods=['POST'])
def set_colours():
    """
    Endpoint to set the LED colours using RGBW values.
    """
    data = request.get_json()
    required_keys = ['red', 'green', 'blue', 'white']
    if not all(key in data for key in required_keys):
        return jsonify({"error": "Missing RGBW values"}), 400

    red_value = data['red']
    green_value = data['green']
    blue_value = data['blue']
    white_value = data['white']

    # Ensure values are in the correct range
    if not all(0 <= value <= 255 for value in [red_value, green_value, blue_value, white_value]):
        return jsonify({"error": "RGBW values must be between 0 and 255"}), 400

    # Update rgbw_values and save settings
    rgbw_values.update({"red": red_value, "green": green_value, "blue": blue_value, "white": white_value})
    save_user_settings()  # Persist RGBW values

    set_led_colours(red_value, green_value, blue_value, white_value)

    return jsonify({"message": f"LED colours set to R: {red_value}, G: {green_value}, B: {blue_value}, W: {white_value}"}), 200

if __name__ == '__main__':
    # Start the background thread for periodic checks
    alarm_thread = Thread(target=periodic_alarm_check)
    alarm_thread.daemon = True  # Allows thread to exit when main program exits
    alarm_thread.start()
    app.run(host=config.HOST, port=config.PORT)