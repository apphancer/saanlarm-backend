import os
import json
from flask import jsonify
from control_state import control_state
from led_control import led_off, set_brightness

USER_SETTINGS_FILE = 'user_settings.json'

# Default states
state = {"state": "off"}
rgbw_values = {"red": 0, "green": 0, "blue": 0, "white": 0}
alarm_time = None

def save_user_settings():
    """
    Save current states (LED state, RGBW values, and alarm time) to the user settings file.
    """
    data = {
        "state": state,
        "rgbw_values": rgbw_values,
        "alarm_time": alarm_time
    }
    with open(USER_SETTINGS_FILE, 'w') as file:
        json.dump(data, file)

def load_user_settings():
    """
    Load user settings from the file. If file does not exist, create a default one.
    """
    global state, rgbw_values, alarm_time
    if not os.path.exists(USER_SETTINGS_FILE):
        save_user_settings()  # Create the file with default values
    else:
        with open(USER_SETTINGS_FILE, 'r') as file:
            data = json.load(file)
            state = data.get("state", state)
            rgbw_values = data.get("rgbw_values", rgbw_values)
            alarm_time = data.get("alarm_time", alarm_time)

def control_led(state):
    """
    Control the LED based on the current state.
    """
    if state.get('state') == "alarm":
        set_brightness(50)
    else:
        led_off()

def get_state():
    """
    Retrieve the current LED state.
    """
    return state

def set_state(data):
    """
    Set the LED state (off, reading, cozy, alarm).
    """
    global state
    if 'state' not in data:
        return jsonify({"error": "State is required"}), 400

    state_value = data['state']
    valid_states = ["off", "reading", "cozy", "alarm"]

    if state_value not in valid_states:
        return jsonify({"error": "Invalid state"}), 400

    # Ensure state is a dictionary
    if isinstance(state, str):  # If state is a string, reset to a valid dictionary
        state = {"state": state_value}
    else:
        state['state'] = state_value  # Update the 'state' in the dictionary

    save_user_settings()  # Persist the state change
    control_state(state)  # Ensure other state-related actions are performed
    control_led(state)  # Control the LED based on the new state

    return jsonify({"message": f"LED state updated to {state_value}"}), 200

def get_alarm_time():
    """
    Get the current alarm time.
    """
    global alarm_time
    if alarm_time:
        return {"alarm_time": alarm_time}
    else:
        return {"message": "No alarm time set"}

def set_alarm_time(data):
    """
    Set the alarm time.
    """
    global alarm_time
    if "alarm_time" not in data:
        return {"error": "Missing 'alarm_time' parameter"}, 400

    alarm_time = data["alarm_time"]
    save_user_settings()  # Persist alarm time

    return {"message": f"Alarm time set to {alarm_time}"}, 200