import sys
import pystray
from PIL import Image
import timer
import os
import threading
import timer_gui

timer_thread = None

def update_icon(icon, item):
    image = Image.open(item)
    icon.icon = image

def quit_app(icon, item):
    timer.isActive = False
    timer.save_data()
    icon.stop()
    sys.exit()

def start_timer(icon, item):
    global timer_thread
    if not timer.isActive:
        timer.isActive = True
        update_icon(icon, 'clock_active.png')
        timer_thread = threading.Thread(target=timer.timer_program, daemon=True)
        timer_thread.start()

def stop_timer(icon, item):
    timer.isActive = False
    update_icon(icon, 'clock.png')
    timer.save_data()

def clean_time_history(icon, item):
    if os.path.exists(timer.json_path):
        timer.window_data = {}
        timer.save_data()

def show_data():
    timer_gui.run_app()

def create_tray_icon():
    image = Image.open('clock.png')
    menu = pystray.Menu(
        pystray.MenuItem('Start timer', start_timer),
        pystray.MenuItem('Stop timer', stop_timer),
        pystray.MenuItem('Show data', show_data),
        pystray.MenuItem('Clean time history', clean_time_history),
        pystray.MenuItem('Exit', quit_app),
    )
    icon = pystray.Icon('TimerTracker', image, menu=menu)
    icon.run_detached()

create_tray_icon()
# timer.timer_program()