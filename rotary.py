from pyky040 import pyky040
import threading

def my_callback(scale_position):
    print('Scale position is {}'.format(scale_position))


my_encoder = pyky040.Encoder(CLK=17, DT=18, SW=26) # todo: move these to config file

def start_rotary():
    my_encoder = pyky040.Encoder(CLK=17, DT=18, SW=26)
    my_encoder.setup(scale_min=0, scale_max=100, step=1, chg_callback=my_callback)
    my_encoder.watch()

def start_rotary_thread():
    rotary_thread = threading.Thread(target=start_rotary)
    rotary_thread.daemon = True
    rotary_thread.start()