from datetime import datetime, timedelta

def check_alarm(state, alarm_time):
    if state != "alarm":
        print("State is not 'alarm'. No action required.")
        return

    if not alarm_time:
        print("No alarm time set.")
        return

    try:
        alarm_time_obj = datetime.strptime(alarm_time, "%H:%M")
    except ValueError:
        print("Invalid alarm time format. Expected HH:MM format.")
        return

    current_time = datetime.now().replace(second=0, microsecond=0)
    alarm_datetime = current_time.replace(hour=alarm_time_obj.hour, minute=alarm_time_obj.minute)

    if alarm_datetime < current_time:
        alarm_datetime += timedelta(days=1)

    time_difference = alarm_datetime - current_time
    if timedelta(minutes=0) <= time_difference <= timedelta(minutes=5):
        print("ALARM STARTING")
    else:
        print(f"Alarm not yet due. Time remaining: {time_difference}")