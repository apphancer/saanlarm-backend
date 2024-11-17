import RPi.GPIO as GPIO
from config import LED_GPIO, LED_GND
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_GPIO, GPIO.OUT)
GPIO.setup(LED_GND, GPIO.OUT)

led_pwm = GPIO.PWM(LED_GPIO, 1000)

def led_on():
    """Turn the LED on at full brightness."""
    led_pwm.start(100)

def led_off():
    """Turn the LED off."""
    led_pwm.stop()

def set_brightness(brightness):
    """Set the brightness of the LED (0-100)."""
    if 0 <= brightness <= 100:
        led_pwm.start(brightness)
    else:
        print("Brightness should be between 0 and 100.")

def cleanup():
    """Clean up GPIO setup."""
    GPIO.cleanup()