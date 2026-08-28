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

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/COM-poort-watcher.git](https://github.com/your-username/COM-poort-watcher.git)
cd COM-poort-watcher
2. Install the required Python packages
Bash
pip install pywin32 pystray pillow pyserial
How to Run the Script
Option A: Run silently in background (Recommended)
Run the script without a visible command prompt / terminal window:

Bash
pythonw com_watcher.pyw
(Or simply double-click the com_watcher.pyw file in Windows Explorer).

Option B: Run with visible console (For debugging)
Bash
python com_watcher.pyw
How to Build a Standalone Executable (.exe)
You can compile the application into a single .exe using PyInstaller so it can run on any Windows machine without Python installed.

1. Install PyInstaller
Bash
pip install pyinstaller
2. Build the optimized .exe
Run the following command to create a compact, single-file executable without opening a console window and excluding unnecessary heavy libraries:

Bash
python -m PyInstaller --noconsole --onefile --exclude-module tkinter --exclude-module matplotlib --exclude-module scipy --exclude-module numpy --exclude-module unittest --exclude-module pydoc com_watcher.pyw
3. Locate your executable
Once the build process completes, your standalone executable com_watcher.exe will be located inside the dist/ folder.

Run on Windows Startup (Optional)
To make the monitor automatically start every time you log in to Windows:

Press Win + R on your keyboard to open the Run dialog.

Type shell:startup and press Enter (this opens your personal Startup folder).

Right-click and choose Create Shortcut (or paste a shortcut) pointing to your com_watcher.exe (or com_watcher.pyw).

How to Close the Application
Right-click the COM icon in your Windows system tray (next to the clock) and click Afsluiten (Exit).

License
This project is open-source and available under the MIT License.
