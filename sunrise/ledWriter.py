import json
import sys
import board
import neopixel
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config_local as config

pixel_pin = getattr(board, f"D{config.LED_DATA_GPIO}")
num_pixels = config.NUM_PIXELS
ORDER = neopixel.GRBW

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, pixel_order=ORDER, auto_write=False)

def set_led_colours_from_json(json_input):
    try:
        led_settings = json.loads(json_input)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    for pixel, colours in led_settings.items():
        try:
            index = int(pixel) - 1  # Convert pixel number to zero-based index
            if 0 <= index < num_pixels:
                red = colours.get("R", 0)
                green = colours.get("G", 0)
                blue = colours.get("B", 0)
                white = colours.get("W", 0)

                # Balance white and RGB to ensure they work together
                if white > 0:
                    total_intensity = max(red, green, blue, white)
                    scaling_factor = min(1.0, 255 / total_intensity)

                    red = int(red * scaling_factor)
                    green = int(green * scaling_factor)
                    blue = int(blue * scaling_factor)
                    white = int(white * scaling_factor)

                pixels[index] = (red, green, blue, white)
        except ValueError:
            print(f"Invalid pixel number: {pixel}")

    pixels.show()

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            set_led_colours_from_json(line.strip())