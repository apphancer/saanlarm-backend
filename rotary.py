import logging
from pyky040 import pyky040
import gpiozero
import threading
import time
from config import ROTARY_SW
from user_settings import load_user_settings, set_alarm_state, get_alarm_state, set_rgbw_values
from alarm_checker import stop_alarm, fade_in_running  # Import the necessary functions and state

logging.basicConfig(level=logging.INFO)

def change_callback(scale_position):
    # Define the brightness levels for each position from 0 to 19
    brightness_levels = {i: int((255 / 19) * i) for i in range(20)}
    brightness = brightness_levels.get(scale_position, 0)

    # Update the brightness in the LED settings by calling set_rgbw_values
    rgbw_data = {"red": 0, "green": 0, "blue": 0, "white": brightness}
    response, status_code = set_rgbw_values(rgbw_data)

    logging.info(f'Scale position {scale_position}, brightness updated to {brightness}')
    print(f'Scale position is {scale_position}, brightness {brightness}, response: {response}, status code: {status_code}')

def sw_callback():
    global fade_in_running  # Use the global fade_in_running flag
    load_user_settings()  # Ensure current settings are loaded
    alarm_state = get_alarm_state()  # Retrieve current alarm state

    if fade_in_running:
        print("Fade-in running, stopping alarm...")
        stop_alarm()
    else:
        if alarm_state == "enabled":
            set_alarm_state("disabled")
            print("Alarm disabled")
        else:
            set_alarm_state("enabled")
            print("Alarm enabled")

EVENT_DEVICE_PATH = '/dev/input/event0'

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