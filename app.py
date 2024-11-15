import os
import json
from flask import Flask, request, jsonify
import led
from alarm_checker import check_alarm  # Import the function

app = Flask(__name__)

USER_SETTINGS_FILE = 'user_settings.json'

# Default states
led_state = {"state": "off"}
rgbw_values = {"red": 0, "green": 0, "blue": 0, "white": 0}
alarm_time = None

def save_user_settings():
    """
    Save current states (LED state, RGBW values, and alarm time) to the user settings file.
    """
    data = {
        "led_state": led_state,
        "rgbw_values": rgbw_values,
        "alarm_time": alarm_time
    }
    with open(USER_SETTINGS_FILE, 'w') as file:
        json.dump(data, file)

def load_user_settings():
    """
    Load user settings from the file. If file does not exist, create a default one.
    """
    global led_state, rgbw_values, alarm_time
    if not os.path.exists(USER_SETTINGS_FILE):
        save_user_settings()  # Create the file with default values
    else:
        with open(USER_SETTINGS_FILE, 'r') as file:
            data = json.load(file)
            led_state = data.get("led_state", led_state)
            rgbw_values = data.get("rgbw_values", rgbw_values)
            alarm_time = data.get("alarm_time", alarm_time)

@app.route('/led-state', methods=['GET'])
def get_led_state():
    """
    Endpoint to get the current state of the LED.
    """
    return jsonify(led_state)

@app.route('/led-state', methods=['POST'])
def set_led_state():
    """
    Endpoint to set the LED state (off, reading, cozy, alarm).
    """
    global led_state
    data = request.get_json()

    if 'state' not in data:
        return jsonify({"error": "State is required"}), 400

    state = data['state']
    valid_states = ["off", "reading", "cozy", "alarm"]

    if state not in valid_states:
        return jsonify({"error": "Invalid state"}), 400

    led_state['state'] = state
    save_user_settings()  # Persist the state change
    control_led(state)

    # Call the alarm checker if the state is relevant
    check_alarm(led_state['state'], alarm_time)

    return jsonify({"message": f"LED state updated to {state}"}), 200

@app.route('/alarm-time', methods=['GET'])
def get_alarm():
    """
    Get the current alarm time.
    """
    global alarm_time
    if alarm_time:
        return jsonify({"alarm_time": alarm_time}), 200
    else:
        return jsonify({"message": "No alarm time set"}), 404

@app.route('/alarm-time', methods=['POST'])
def set_alarm():
    """
    Set the alarm time.
    """
    global alarm_time
    data = request.get_json()
    if "alarm_time" not in data:
        return jsonify({"error": "Missing 'alarm_time' parameter"}), 400

    alarm_time = data["alarm_time"]
    save_user_settings()  # Persist alarm time

    # Check the alarm after setting the time (in case state is "alarm")
    check_alarm(led_state['state'], alarm_time)

    return jsonify({"message": f"Alarm time set to {alarm_time}"}), 200

@app.route('/colours', methods=['POST'])
def set_colours():
    """
    Endpoint to set the LED colour using RGBW values.
    """
    global rgbw_values
    data = request.get_json()

    required_keys = ['red', 'green', 'blue', 'white']
    if not all(key in data for key in required_keys):
        return jsonify({"error": "Missing RGBW values"}), 400

    red_value = data['red']
    green_value = data['green']
    blue_value = data['blue']
    white_value = data['white']

    if not all(0 <= value <= 255 for value in [red_value, green_value, blue_value, white_value]):
        return jsonify({"error": "RGBW values must be between 0 and 255"}), 400

    rgbw_values = {"red": red_value, "green": green_value, "blue": blue_value, "white": white_value}
    save_user_settings()  # Persist RGBW values

    led.set_led_colours(red_value, green_value, blue_value, white_value)

    return jsonify({"message": f"LED colours set to R: {red_value}, G: {green_value}, B: {blue_value}, W: {white_value}"}), 200

@app.route('/colours', methods=['GET'])
def get_colours():
    """
    Endpoint to get the current RGBW values.
    """
    return jsonify(rgbw_values)

if __name__ == '__main__':
    load_user_settings()
    app.run(host='0.0.0.0', port=5000)