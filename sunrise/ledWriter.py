import json
import sys
import board
import neopixel

NUM_PIXELS = 150
LED_DATA_GPIO = 21
ORDER = neopixel.GRBW

pixel_pin = getattr(board, f"D{LED_DATA_GPIO}")
pixels = neopixel.NeoPixel(pixel_pin, NUM_PIXELS, pixel_order=ORDER, auto_write=False)

def set_led_colours_from_json(json_input):
    try:
        led_settings = json.loads(json_input)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    for pixel, colours in led_settings.items():
        try:
            index = int(pixel) - 1  # Convert pixel number to zero-based index
            if 0 <= index < NUM_PIXELS:
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

def set_led_colours_from_json_input():
    json_input = sys.stdin.read()
    set_led_colours_from_json(json_input)

if __name__ == "__main__":
    set_led_colours_from_json_input()