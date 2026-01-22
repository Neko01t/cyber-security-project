import platform
import os
from datetime import datetime

log_file = "keylog.txt"

# Detect OS
def detect_os():
    return platform.system()

# Detect Display Server (Wayland / X11)
def detect_display():
    if os.environ.get("WAYLAND_DISPLAY"):
        return "Wayland"
    elif os.environ.get("DISPLAY"):
        return "X11"
    return "Unknown"

# Log function
def log_key(key):
    with open(log_file, "a") as f:
        f.write(key)

def main():
    os_name = detect_os()
    display = detect_display()

    print("="*50)
    print(" Python Demonstration Keylogger ")
    print("="*50)
    print(f"OS Detected      : {os_name}")
    print(f"Display Server   : {display}")

    if os_name == "Linux" and display == "Wayland":
        print("WARNING: Global keylogging is restricted by Wayland security.")
        print("Running in DEMONSTRATION MODE (terminal capture).")

    print("\nType anything. Press CTRL+C to stop.\n")

    with open(log_file, "a") as f:
        f.write(f"\n--- Logging started at {datetime.now()} ---\n")
        f.write(f"OS: {os_name}, Display: {display}\n")

    try:
        while True:
            key = input("> ")   # live visible demo
            print(f"[LOGGED] {key}")
            log_key(key + "\n")
    except KeyboardInterrupt:
        print("\nKeylogger stopped.")
        with open(log_file, "a") as f:
            f.write("--- Logging stopped ---\n")

if __name__ == "__main__":
    main()

