import os
import json
from flask import jsonify
from led_control import led_off, set_brightness
from led import set_led_colours

USER_SETTINGS_FILE = 'user_settings.json'

state = {"state": "off"}
rgbw_values = {"red": 0, "green": 0, "blue": 0, "white": 0}
alarm_time = None

def save_user_settings():
    data = {
        "state": state,
        "rgbw_values": rgbw_values,
        "alarm_time": alarm_time
    }
    with open(USER_SETTINGS_FILE, 'w') as file:
        json.dump(data, file)

def load_user_settings():
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
    if state.get('state') == "alarm":
        set_brightness(5)
    else:
        led_off()

def get_state():
    return state

def set_state(data):
    global state
    if 'state' not in data:
        return jsonify({"error": "State is required"}), 400

    state_value = data['state']
    valid_states = ["off", "reading", "cozy", "alarm"]

    if state_value not in valid_states:
        return jsonify({"error": "Invalid state"}), 400

    if isinstance(state, str):
        state = {"state": state_value}
    else:
        state['state'] = state_value

    save_user_settings()
    control_led(state)

    return jsonify({"message": f"LED state updated to {state_value}"}), 200

def get_alarm_time():
    global alarm_time
    if alarm_time:
        return {"alarm_time": alarm_time}
    else:
        return {"message": "No alarm time set"}

def set_alarm_time(data):
    global alarm_time
    if "alarm_time" not in data:
        return {"error": "Missing 'alarm_time' parameter"}, 400

    alarm_time = data["alarm_time"]
    save_user_settings()

    return {"message": f"Alarm time set to {alarm_time}"}, 200


def get_rgbw_values():
    global rgbw_values
    load_user_settings()
    return rgbw_values

def set_rgbw_values(data):
    global rgbw_values
    required_keys = ['red', 'green', 'blue', 'white']
    if not all(key in data for key in required_keys):
        return {"error": "Missing RGBW values"}, 400

    if not all(0 <= data[key] <= 255 for key in required_keys):
        return {"error": "RGBW values must be between 0 and 255"}, 400

    rgbw_values.update({key: data[key] for key in required_keys})
    save_user_settings()

    set_led_colours(
        rgbw_values['red'],
        rgbw_values['green'],
        rgbw_values['blue'],
        rgbw_values['white']
    )

    return {"message": "RGBW values updated successfully"}, 200