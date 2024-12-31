from datetime import datetime, timedelta
import time
import config_local as config
from user_settings import set_rgbw_values, set_alarm_state, get_alarm_time
from threading import Event
from logger import log_with_datetime
from sunrise.shuffledCycleGenerator import start_sunrise_cycle

fade_in_running_event = Event()
alarm_triggered = False
running = False

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

    duration_minutes = (config.SUNRISE_PHASE_1_TOTAL_MINUTES + config.SUNRISE_PHASE_2_TOTAL_MINUTES + config.SUNRISE_PHASE_3_TOTAL_MINUTES)

    if timedelta(minutes=0) <= time_difference <= timedelta(minutes=duration_minutes):
        return "ALARM STARTING"
    else:
        return f"Alarm not yet due. Time remaining: {time_difference}"

def fade_in_led(callback):
    fade_in_running_event.set()

    try:
        start_sunrise_cycle(fade_in_running_event)
    except Exception as e:
        log_with_datetime(f"Error during sunrise cycle: {e}")
        fade_in_running_event.clear()

    if fade_in_running_event.is_set():
        callback()

def stop_alarm():
    fade_in_running_event.clear()
    set_alarm_state("disabled")
    rgbw_data = {"red": 0, "green": 0, "blue": 0, "white": 0}
    response, status_code = set_rgbw_values(rgbw_data)
    log_with_datetime("ALARM STOPPED")

def periodic_alarm_check():
    global running, alarm_triggered
    running = True

    while running:
        alarm_info = get_alarm_time()
        alarm_time = alarm_info['alarm_time']
        alarm_state = alarm_info['alarm_state']


        log_with_datetime(f"Checking alarm. Alarm triggered: {alarm_triggered}")

        if alarm_state == "enabled" and alarm_time:
            result = check_alarm(alarm_state, alarm_time)
            if result == "ALARM STARTING" and not alarm_triggered:
                log_with_datetime(result)
                alarm_triggered = True
                if not fade_in_running_event.is_set():
                    fade_in_led(fade_in_completed)
            elif result != "ALARM STARTING":
                alarm_triggered = False
                if fade_in_running_event.is_set():
                    stop_alarm()
        time.sleep(60)

def fade_in_completed():
    fade_in_running_event.clear()
