from datetime import datetime, timedelta

def check_alarm(state, alarm_time):
    """
    Checks if the alarm should trigger based on the state and current time.
    Prints a message if the alarm is starting.
    """
    if state != "alarm":
        print("State is not 'alarm'. No action required.")
        return

    # Check if alarm time is set
    if not alarm_time:
        print("No alarm time set.")
        return

    try:
        alarm_time_obj = datetime.strptime(alarm_time, "%H:%M")
    except ValueError:
        print("Invalid alarm time format. Expected HH:MM format.")
        return

    # Get current time
    current_time = datetime.now().replace(second=0, microsecond=0)
    alarm_datetime = current_time.replace(hour=alarm_time_obj.hour, minute=alarm_time_obj.minute)

    # Handle case where alarm time might be for the next day
    if alarm_datetime < current_time:
        alarm_datetime += timedelta(days=1)

    # Check if the current time is within 5 minutes of the alarm time
    time_difference = alarm_datetime - current_time
    if timedelta(minutes=0) <= time_difference <= timedelta(minutes=5):
        print("ALARM STARTING")
    else:
        print(f"Alarm not yet due. Time remaining: {time_difference}")