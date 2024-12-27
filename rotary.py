import logging
from pyky040 import pyky040
import gpiozero
import threading
import time
from config import ROTARY_SW
from user_settings import load_user_settings, set_alarm_state, get_alarm_state, set_rgbw_values
from alarm_checker import stop_alarm, fade_in_running_event
from logger import log_with_datetime
import os
import evdev

logging.basicConfig(level=logging.INFO)

def get_rotary_device():
    print("Scanning available input devices...")

    for event_file in os.listdir('/dev/input/'):
        if event_file.startswith('event'):  # Look at input event files
            try:
                device = evdev.InputDevice(f'/dev/input/{event_file}')
                print(f"Found device: {device.name} at /dev/input/{event_file}")  # Log all found devices

                # Match the rotary encoder's name as described in your system (from dmesg)
                if device.name == "rotary@11":
                    return f"/dev/input/{event_file}"
            except Exception as e:
                print(f"Skipping {event_file}: {e}")  # Log skipped files if any
                continue

    # If no matching device is found, raise an exception
    raise Exception("Rotary encoder device not found!")

def change_callback(scale_position):
    brightness_levels = {i: int((255 / 19) * i) for i in range(20)}
    brightness = brightness_levels.get(scale_position, 0)

    rgbw_data = {"red": 0, "green": 0, "blue": 0, "white": brightness}
    set_rgbw_values(rgbw_data)

    logging.info(f'Scale position {scale_position}, brightness updated to {brightness}')
    log_with_datetime(f'Scale position is {scale_position}, brightness {brightness}')

def sw_callback():
    load_user_settings()
    alarm_state = get_alarm_state()

    if fade_in_running_event.is_set():
        log_with_datetime("Fade-in running, stopping alarm...")
        stop_alarm()
    else:
        if alarm_state == "enabled":
            set_alarm_state("disabled")
            log_with_datetime("Alarm disabled")
        else:
            set_alarm_state("enabled")
            log_with_datetime("Alarm enabled")

try:
   EVENT_DEVICE_PATH = get_rotary_device()
   print(f"Rotary encoder device found: {EVENT_DEVICE_PATH}")
except Exception as e:
   print(f"Error: {e}")
   exit(1)

try:
    my_encoder = pyky040.Encoder(device=EVENT_DEVICE_PATH)
    logging.info("Encoder initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize encoder: {e}")
    exit(1)

switch = gpiozero.Button(ROTARY_SW)

def start_rotary():
    try:
        my_encoder.setup(scale_min=0, scale_max=19, step=1, loop=True, chg_callback=change_callback)
        my_encoder.watch()
        logging.info("Rotary encoder setup and watching for changes.")
    except Exception as e:
        logging.error(f"Failed to setup/watch encoder: {e}")

def start_rotary_thread():
    rotary_thread = threading.Thread(target=start_rotary)
    rotary_thread.daemon = True
    rotary_thread.start()

switch.when_pressed = sw_callback

if __name__ == "__main__":
    logging.info("Starting rotary encoder thread.")
    start_rotary_thread()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Program interrupted by user. Exiting...")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")