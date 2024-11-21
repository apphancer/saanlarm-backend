from datetime import datetime

def log_with_datetime(message):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{current_time} | {message}")