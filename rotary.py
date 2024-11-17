from pyky040 import pyky040
import threading
from config import ROTARY_CLK, ROTARY_DT, ROTARY_SW

def my_callback(scale_position):
    print('Scale position is {}'.format(scale_position))

my_encoder = pyky040.Encoder(CLK=ROTARY_CLK, DT=ROTARY_DT, SW=ROTARY_SW)

def start_rotary():
    my_encoder.setup(scale_min=0, scale_max=100, step=1, chg_callback=my_callback)
    my_encoder.watch()

def start_rotary_thread():
    rotary_thread = threading.Thread(target=start_rotary)
    rotary_thread.daemon = True
    rotary_thread.start()