# alarm_checker.py

from user_settings import get_alarm_time
from .led_control import fade_in_led  # Assuming fade_in_led is in an appropriate module
import time

fade_in_running = False  # Ensure this flag is properly scoped

alarm_triggered = False  # Flag to ensure the alarm starts only once

def periodic_alarm_check(alarm_triggered, fade_in_running):
    running = True

    while running:
        alarm_info = get_alarm_time()
        alarm_time = alarm_info['alarm_time']
        alarm_state = alarm_info['alarm_state']

        # Perform the alarm check
        if alarm_state == "enabled" and alarm_time:
            result = check_alarm(alarm_state, alarm_time)
            if result == "ALARM STARTING" and not alarm_triggered:
                print(result)  # Print ALARM STARTING only once
                alarm_triggered = True
                if not fade_in_running:
                    fade_in_led(fade_in_completed)
            elif result != "ALARM STARTING":
                alarm_triggered = False  # Reset the flag if not in the alarm window
                if fade_in_running:
                    fade_in_running = False
                    print("ALARM STOPPED")
        time.sleep(60)

def fade_in_completed():
    global fade_in_running
    fade_in_running = False
    print("ALARM STOPPED")