# Windows COM Port Monitor (COM Watcher)

A lightweight Windows system tray application that monitors active COM ports (including USB virtual serial ports like Arduino, FTDI, CH340, ESP32, etc.) in real time using native Windows hardware events.

---

## Features

- **System Tray Icon:** Sits unobtrusively next to the Windows clock with a custom `COM` icon.
- **Instant Connection Popups:** Native Windows notifications appear immediately when a new COM port is connected.
- **Hover Tooltip:** Hovering over the tray icon displays a list of all currently connected COM ports.
- **Context Menu Details:** Right-click to inspect detailed hardware information per port:
  - Description & Manufacturer
  - USB VID:PID
  - Serial Number
  - Hardware ID (HWID)
- **Quick Access:** Directly open Windows Device Manager (`devmgmt.msc`) from the context menu.
- **Lightweight & Efficient:** Event-driven via Windows `WM_DEVICECHANGE` API (no heavy continuous polling).

---

## Prerequisites

- **OS:** Windows 10 / 11
- **Python:** Python 3.8 or higher

---

## Installation & Dependencies

**Clone the repository:**
```bash
git clone [https://github.com/your-username/com-poort-watcher.git](https://github.com/your-username/com-poort-watcher.git)
cd com-poort-watcher



Install the required Python packages:
pip install pywin32 pystray pillow pyserial



To run silently in the background without a terminal window:
python com_watcher.pyw



You can package the application into a single standalone .exe using PyInstaller. This allows you to run it on any Windows PC without needing Python installed:
pip install pyinstaller



**Build the exe file**
Run the following command to create a compact, single-file executable without opening a console window:
python -m PyInstaller --noconsole --onefile --exclude-module tkinter --exclude-module matplotlib --exclude-module scipy --exclude-module numpy --exclude-module unittest --exclude-module pydoc com_watcher.pyw
