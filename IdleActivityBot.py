import ctypes
import time
import random
import threading
import pyautogui
import psutil
import os
import logging

# Настройка логирования
log_path = os.path.join(os.getenv('TEMP'), 'work_time_bot.log')
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def get_idle_duration():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    else:
        return 0

def simulate_activity(stop_event):
    original_pos = pyautogui.position()
    try:
        while not stop_event.is_set():
            action = random.choice(['move', 'click', 'keypress', 'window_switch'])
            logging.info(f'Executing action: {action}')
            if action == 'move':
                x = original_pos.x + random.randint(-10, 10)
                y = original_pos.y + random.randint(-10, 10)
                pyautogui.moveTo(x, y, duration=0.5)
            elif action == 'click':
                pyautogui.click()
            elif action == 'keypress':
                key = random.choice(['shift', 'ctrl', 'alt'])
                pyautogui.keyDown(key)
                time.sleep(0.1)
                pyautogui.keyUp(key)
            elif action == 'window_switch':
                pyautogui.hotkey('alt', 'tab')
                time.sleep(1)
                pyautogui.hotkey('alt', 'tab')
            elif action == 'temp_file':
                temp_path = os.path.join(os.getenv('TEMP'), f'tempfile_{random.randint(1000,9999)}.txt')
                with open(temp_path, 'w') as f:
                    f.write('temporary')
                os.remove(temp_path)
            time.sleep(random.uniform(5, 15))
    finally:
        pyautogui.moveTo(original_pos)
        logging.info('Stopped simulating activity')

def main_loop():
    stop_event = threading.Event()
    activity_thread = None
    while True:
        idle = get_idle_duration()
        logging.info(f'Idle duration: {idle:.2f} seconds')
        if idle > 90:
            if activity_thread is None or not activity_thread.is_alive():
                logging.info('Starting activity thread')
                stop_event.clear()
                activity_thread = threading.Thread(target=simulate_activity, args=(stop_event,), daemon=True)
                activity_thread.start()
        else:
            if activity_thread is not None and activity_thread.is_alive():
                logging.info('Stopping activity thread')
                stop_event.set()
                activity_thread.join()
                activity_thread = None
        time.sleep(5)

if __name__ == "__main__":
    main_loop()
