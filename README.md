# Smart Auto Mouse Mover

**Smart Auto Mouse Mover** is a lightweight Python-based tool that simulates mouse activity to prevent screen locks during idle periods. It intelligently detects user activity, such as mouse movements and keyboard input, ensuring it doesn't interfere with active usage. Ideal for remote work, presentations, and keeping sessions alive.

## Features

- Simulates small mouse movements every 20 seconds of inactivity.
- Detects keyboard and mouse activity to avoid unnecessary interference.
- Runs quietly in the background with minimal resource usage.
- Includes a system tray icon for easy control.
- Detects screen lock state and pauses movements automatically.

## Requirements

- Python 3.7+
- Libraries:
  - `pyautogui`
  - `pynput`
  - `pystray`
  - `Pillow`
  - `psutil`

Install dependencies with:
```bash
pip install pyautogui pynput pystray pillow psutil
