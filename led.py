import board
import neopixel
import config_local as config

pixel_pin = getattr(board, f"D{config.LED_DATA_GPIO}")
num_pixels = config.NUM_PIXELS
ORDER = neopixel.GRBW

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, pixel_order=ORDER, auto_write=False)

def set_led_colours(red, green, blue, white):
    print(f"Setting LED colours to R:{red} G:{green} B:{blue} W:{white}")
    for i in range(num_pixels):
        pixels[i] = (red, green, blue, white)
    pixels.show()