import os
import json
from flask import Flask, request, jsonify
import led

app = Flask(__name__)

ALARM_CONFIG_FILE = 'alarm_config.json'

# Default LED state
led_state = {"state": "off"}

@app.route('/led-state', methods=['GET'])
def get_led_state():
    """
    Endpoint to get the current state of the LED
    """
    return jsonify(led_state)

@app.route('/led-state', methods=['POST'])
def set_led_state():
    """
    Endpoint to set the LED state (off, reading, cozy, alarm)
    """
    data = request.get_json()

    # Check if 'state' key exists in the request
    if 'state' not in data:
        return jsonify({"error": "State is required"}), 400

    state = data['state']

    # Validating state
    valid_states = ["off", "reading", "cozy", "alarm"]
    if state not in valid_states:
        return jsonify({"error": "Invalid state"}), 400

    # Update the LED state and simulate control
    led_state['state'] = state
    control_led(state)

    return jsonify({"message": f"LED state updated to {state}"}), 200

@app.route('/alarm-time', methods=['GET'])
def get_alarm():
    """Get the current alarm time."""
    alarm_time = get_alarm_time()
    if alarm_time:
        return jsonify({"alarm_time": alarm_time}), 200
    else:
        return jsonify({"message": "No alarm time set"}), 404

@app.route('/alarm-time', methods=['POST'])
def set_alarm():
    """Set the alarm time."""
    data = request.get_json()
    if "alarm_time" not in data:
        return jsonify({"error": "Missing 'alarm_time' parameter"}), 400

    alarm_time = data["alarm_time"]
    set_alarm_time(alarm_time)
    return jsonify({"message": f"Alarm time set to {alarm_time}"}), 200


@app.route('/set-colours', methods=['POST'])
def set_colours():
    """
    Endpoint to set the LED colour using RGBW values
    """
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

    led.set_led_colours(red_value, green_value, blue_value, white_value)

    return jsonify({"message": f"LED colours set to R: {red_value}, G: {green_value}, B: {blue_value}, W: {white_value}"}), 200



def control_led(state):
    """
    Function to control the LED based on the state
    """

    if state == "off":
        print("Turning off LED")
    elif state == "reading":
        print("Setting LED to 100% brightness")
    elif state == "cozy":
        print("Setting LED to 50% brightness")
    elif state == "alarm":
        print("Setting up alarm activation")
    else:
        print("Unknown state")

def get_alarm_time():
    if not os.path.exists(ALARM_CONFIG_FILE):
        with open(ALARM_CONFIG_FILE, 'w') as file:
            json.dump({"alarm_time": None}, file)
        return None

    with open(ALARM_CONFIG_FILE, 'r') as file:
        data = json.load(file)
    return data.get("alarm_time")

def set_alarm_time(alarm_time):
    with open(ALARM_CONFIG_FILE, 'w') as file:
        json.dump({"alarm_time": alarm_time}, file)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)