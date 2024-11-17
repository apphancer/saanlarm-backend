import os
import json
from flask import jsonify
from led_control import led_off, set_brightness
from led import set_led_colours

USER_SETTINGS_FILE = 'user_settings.json'

rgbw_values = {"red": 0, "green": 0, "blue": 0, "white": 0}
alarm_time = None
alarm_state = "disabled"

def save_user_settings():
    data = {
        "rgbw_values": rgbw_values,
        "alarm_time": alarm_time,
        "alarm_state": alarm_state
    }
    with open(USER_SETTINGS_FILE, 'w') as file:
        json.dump(data, file)

def load_user_settings():
    global rgbw_values, alarm_time, alarm_state
    if not os.path.exists(USER_SETTINGS_FILE):
        save_user_settings()  # Create the file with default values
    else:
        with open(USER_SETTINGS_FILE, 'r') as file:
            data = json.load(file)
            rgbw_values = data.get("rgbw_values", rgbw_values)
            alarm_time = data.get("alarm_time", alarm_time)
            alarm_state = data.get("alarm_state", alarm_state)

def control_led(alarm_state):
    if alarm_state == "enabled":
        set_brightness(5)
    else:
        led_off()

def get_alarm_time():
    global alarm_time, alarm_state
    return {"alarm_time": alarm_time, "alarm_state": alarm_state}

def set_alarm_time(data):
    global alarm_time
    if "alarm_time" not in data or "alarm_state" not in data:
        return {"error": "Missing 'alarm_time' or 'alarm_state' parameter"}, 400

    alarm_time = data["alarm_time"]
    set_alarm_state(data["alarm_state"])

    return {"message": f"Alarm time set to {alarm_time} and state set to {alarm_state}"}, 200

def set_alarm_state(state):
    global alarm_state
    alarm_state = state
    save_user_settings()
    control_led(alarm_state)

def get_alarm_state():
    global alarm_state
    return alarm_state

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