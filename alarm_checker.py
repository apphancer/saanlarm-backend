from datetime import datetime, timedelta
import time
import config
from user_settings import set_rgbw_values, set_alarm_state, get_alarm_time
import threading

fade_in_lock = threading.Lock()
fade_in_running = False  # Flag to track fade-in state
alarm_triggered = False  # Flag to ensure the alarm starts only once
running = False  # Ensure that the periodic alarm checker runs

def check_alarm(alarm_state, alarm_time):
    if alarm_state != "enabled":
        return "Alarm is not enabled. No action required."

    if not alarm_time:
        return "No alarm time set."

    try:
        alarm_time_obj = datetime.strptime(alarm_time, "%H:%M")
    except ValueError:
        return "Invalid alarm time format. Expected HH:MM format."

    current_time = datetime.now().replace(second=0, microsecond=0)
    alarm_datetime = current_time.replace(hour=alarm_time_obj.hour, minute=alarm_time_obj.minute)

    if alarm_datetime < current_time:
        alarm_datetime += timedelta(days=1)

    time_difference = alarm_datetime - current_time
    duration_minutes = config.LED_FADE_IN_DURATION_MINUTES

    if timedelta(minutes=0) <= time_difference <= timedelta(minutes=duration_minutes):
        return "ALARM STARTING"
    else:
        return f"Alarm not yet due. Time remaining: {time_difference}"

def fade_in_led(callback):
    global fade_in_running
    with fade_in_lock:
        fade_in_running = True

    print(f"Fade-in started: fade_in_running = {fade_in_running}")  # Debugging
    duration_seconds = config.LED_FADE_IN_DURATION_MINUTES * 60  # convert minutes to seconds
    steps = 255
    step_duration = duration_seconds / steps

    for brightness in range(steps):
        with fade_in_lock:
            if not fade_in_running:
                break


        rgbw_data = {"red": 0, "green": 0, "blue": 0, "white": brightness}
        response, status_code = set_rgbw_values(rgbw_data)
        time.sleep(step_duration)  # wait for the next step

    with fade_in_lock:
        if fade_in_running:
            callback()
    print(f"Fade-in completed: fade_in_running = {fade_in_running}")  # Debugging

def stop_alarm():
    global fade_in_running
    fade_in_running = False
    set_alarm_state("disabled")
    rgbw_data = {"red": 0, "green": 0, "blue": 0, "white": 0}  # todo: maybe instead of turning off, we turn to the last stored setting?
    response, status_code = set_rgbw_values(rgbw_data)
    print("ALARM STOPPED")

def periodic_alarm_check():
    global running, alarm_triggered, fade_in_running
    running = True

    while running:
        alarm_info = get_alarm_time()
        alarm_time = alarm_info['alarm_time']
        alarm_state = alarm_info['alarm_state']

        # Debugging
        print(f"Checking alarm. Alarm triggered: {alarm_triggered}, fade_in_running: {fade_in_running}")

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
    print("Fade-in completed: fade_in_running set to False")  # Debugging