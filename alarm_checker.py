from datetime import datetime, timedelta

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
    if timedelta(minutes=0) <= time_difference <= timedelta(minutes=5):
        return "ALARM STARTING"
    else:
        return f"Alarm not yet due. Time remaining: {time_difference}"

# Example usage
if __name__ == "__main__":
    alarm_state = "enabled"  # This should ideally come from the JSON data
    alarm_time = "14:30"     # This should also come from the JSON data

    result = check_alarm(alarm_state, alarm_time)
    print(result)