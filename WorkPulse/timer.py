import win32gui
import win32process
import psutil
import time
import json
import os

# checks if the app is still running
isActive = False
json_path = 'timer_data.json'

if os.path.exists(json_path):
    with open(json_path, 'r') as f:
        window_data = json.load(f)
else:
    window_data = {}

def timer_program():
    global window_data, isActive
    last_time = time.perf_counter()
    remainder = 0.0

    while isActive:
        current_time = time.perf_counter()
        elapsed = current_time - last_time
        last_time = current_time

        elapsed += remainder
        whole_seconds = int(elapsed)
        remainder = elapsed - whole_seconds

        if whole_seconds > 0:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            try:
                process = psutil.Process(pid).name().replace('.exe', '').capitalize()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

            if process not in window_data:
                window_data[process] = 0
            window_data[process] += whole_seconds

            print(window_data)
            save_data()
        time.sleep(0.1)

def save_data():
    with open(json_path, "w") as f:
        json.dump(window_data, f, indent=4)