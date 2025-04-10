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
    while isActive:
        # hwnd - Handle to a window, a unique id for an active window in Windows, it occurs as an integer, e.g. 123456
        # Gets an id of an active window
        hwnd = win32gui.GetForegroundWindow()

        # Gets thread id and process id, here the thread id is useless
        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        try:
            # Uses window id and process id to get the name of an active process/window e.g. pycharm.exe
            process = psutil.Process(pid).name().replace('.exe', '').capitalize()

            # Gets the name of an active window e.g. NewProject - timer.py
            window_name = win32gui.GetWindowText(hwnd)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

        if process not in window_data:
            window_data[process] = 0
        window_data[process] += 1
        time.sleep(1)

        print(window_data)
        save_data()

def save_data():
    with open(json_path, "w") as f:
        json.dump(window_data, f, indent=4)