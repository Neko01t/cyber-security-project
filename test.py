from pynput.keyboard import Key, Listener
import evdev

device = evdev.InputDevice('/dev/input/event3')

print(f"Listening on {device.name}...")

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        print(evdev.categorize(event))
def on_press(key):
    # Added flush=True to force output immediately
    print("{0} pressed".format(key), flush=True)

def on_release(key):
    if key == Key.esc:
        return False

# Changed 'as Listener' to 'as listener' to avoid naming conflict
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
