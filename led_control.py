import RPi.GPIO as GPIO
from config import LED_GPIO, LED_GND
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED_GPIO, GPIO.OUT)
GPIO.setup(LED_GND, GPIO.OUT)

led_pwm = GPIO.PWM(LED_GPIO, 1000)

def led_on():
    led_pwm.start(100)

def led_off():
    led_pwm.stop()

def set_brightness(brightness):
    if 0 <= brightness <= 100:
        led_pwm.start(brightness)
    else:
        print("Brightness should be between 0 and 100.")

def cleanup():
    GPIO.cleanup()