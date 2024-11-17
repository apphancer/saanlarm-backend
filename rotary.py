from pyky040 import pyky040
import threading
from config import ROTARY_CLK, ROTARY_DT, ROTARY_SW

def my_callback(scale_position):
    global last_update_time
    current_time = time.time()

    # Implement debounce: ignore changes if they are too close to the previous update
    if current_time - last_update_time < DEBOUNCE_TIME:
        return  # Skip this callback to prevent double logging

    # Update the last update time
    last_update_time = current_time

    # Handle the scale position to reset after reaching the max value of 20
    scale_position = scale_position % 21  # Modulo 21 to reset after 20
    print('Scale position is {}'.format(scale_position))

my_encoder = pyky040.Encoder(CLK=ROTARY_CLK, DT=ROTARY_DT, SW=ROTARY_SW)

def start_rotary():
    my_encoder.setup(scale_min=0, scale_max=20, step=1, chg_callback=my_callback)
    my_encoder.watch()

def start_rotary_thread():
    rotary_thread = threading.Thread(target=start_rotary)
    rotary_thread.daemon = True
    rotary_thread.start()