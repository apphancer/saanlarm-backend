# led_control.py
import RPi.GPIO as GPIO
from config import LED_GPIO, LED_GND
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the LED pin as output
GPIO.setup(LED_GPIO, GPIO.OUT)
GPIO.setup(LED_GND, GPIO.OUT)  # Make sure the ground is connected to GND

# Set PWM control
led_pwm = GPIO.PWM(LED_GPIO, 1000)  # 1kHz frequency for PWM

def led_on():
    """Turn the LED on at full brightness."""
    led_pwm.start(100)  # Full brightness (100%)

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

if __name__ == "__main__":
    try:
        led_on()
        time.sleep(5)  # LED on for 5 seconds
        led_off()
        time.sleep(2)  # Wait for 2 seconds
        set_brightness(50)  # Set brightness to 50%
        time.sleep(5)  # Wait for 5 seconds
    finally:
        cleanup()