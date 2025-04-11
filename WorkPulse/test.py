import time
import threading
from pynput import mouse, keyboard

# Globalne zmienne
last_activity_time = time.time()  # Czas ostatniej aktywności
inactive_time_limit = 5  # Sekundy bezczynności przed zatrzymaniem stopera
is_active = True  # Flaga do kontrolowania aktywności stopera
timer_start_time = 0  # Czas, od którego zaczyna liczyć stoper
elapsed_time = 0  # Całkowity czas działania stopera

# Funkcja monitorująca nieaktywność
def monitor_inactivity():
    global last_activity_time, is_active, elapsed_time
    while True:
        if time.time() - last_activity_time > inactive_time_limit:
            if is_active:
                print(f"Zatrzymano stoper, czas: {elapsed_time} sekund")
                is_active = False
        time.sleep(1)

# Funkcja, która restartuje stoper po aktywności
def on_move(x, y):
    global last_activity_time, is_active, timer_start_time, elapsed_time
    last_activity_time = time.time()
    if not is_active:
        is_active = True
        timer_start_time = time.time()  # Rozpocznij nowy stoper
        print("Wznawianie stopera...")

def on_click(x, y, button, pressed):
    global last_activity_time, is_active, timer_start_time, elapsed_time
    last_activity_time = time.time()
    if not is_active:
        is_active = True
        timer_start_time = time.time()  # Rozpocznij nowy stoper
        print("Wznawianie stopera...")

# Funkcja stopera
def stopwatch():
    global is_active, timer_start_time, elapsed_time
    while True:
        if is_active:
            elapsed_time = time.time() - timer_start_time
            print(f"Czas: {elapsed_time:.2f} sekundy")
        time.sleep(0.1)

# Uruchomienie wątków
def start():
    # Monitorowanie nieaktywności
    inactivity_thread = threading.Thread(target=monitor_inactivity, daemon=True)
    inactivity_thread.start()

    # Stoper
    stopwatch_thread = threading.Thread(target=stopwatch, daemon=True)
    stopwatch_thread.start()

    # Monitorowanie aktywności myszy i klawiatury
    with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
        listener.join()

    with keyboard.Listener(on_click=on_click) as listener:
        listener.join()

# Rozpocznij program
start()
