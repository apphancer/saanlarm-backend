import logging
from pyky040 import pyky040
import gpiozero
import threading
import time
from config import ROTARY_SW

logging.basicConfig(level=logging.INFO)

def change_callback(scale_position):
    print('Scale position is {}'.format(scale_position))

def sw_callback():
    print('Switch pressed!')

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