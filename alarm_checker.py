from datetime import datetime, timedelta
import time
import config
from user_settings import set_rgbw_values, set_alarm_state

fade_in_running = False  # Flag to track fade-in state

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
    fade_in_running = True
    duration_seconds = config.LED_FADE_IN_DURATION_MINUTES * 60  # convert minutes to seconds
    steps = 255
    step_duration = duration_seconds / steps

    for brightness in range(steps):
        rgbw_data = {"red": 0, "green": 0, "blue": 0, "white": brightness}
        response, status_code = set_rgbw_values(rgbw_data)
        time.sleep(step_duration)  # wait for the next step

    callback()

def stop_alarm():
    global fade_in_running
    set_alarm_state("disabled")
    rgbw_data = {"red": 0, "green": 0, "blue": 0, "white": 0} # todo: maybe instead of turning off, we turn to the last stored setting?
    response, status_code = set_rgbw_values(rgbw_data)
    fade_in_running = False
    print("ALARM STOPPED")