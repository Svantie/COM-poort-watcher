# Windows COM Port Monitor (COM Watcher)

A lightweight Windows system tray application that monitors active COM ports (including USB virtual serial ports like Arduino, FTDI, CH340, ESP32, etc.) in real time using native Windows hardware events.

---

## Features

- **System Tray Icon:** Sits unobtrusively next to the Windows clock with a custom blue `COM` icon.
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

- **Operating System:** Windows 10 or Windows 11
- **Python Version:** Python 3.8 or higher

---

## Step 1: Installation (cloining the repository)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/COM-poort-watcher.git](https://github.com/your-username/COM-poort-watcher.git)
   cd COM-poort-watcher


## Step 2: Install Dependencies

1. **Clone the repository:**
   ```bash
   pip install pywin32 pystray pillow pyserial


2. **Running the application:**
   ```bash
   pythonw com_watcher.pyw

3. **Installing pyinstaller to build a standalone exe:**
   ```bash
   pip install pyinstaller

4. **Buildng the executable:**
   ```bash
   python -m PyInstaller --noconsole --onefile --exclude-module tkinter --exclude-module matplotlib --exclude-module scipy --exclude-module numpy --exclude-module unittest --exclude-module pydoc com_watcher.pyw
  
5. **Running on windows startup:**

Press Win + R to open the Run prompt.
Type shell:startup and press Enter.
Create a shortcut to com_watcher.exe (or com_watcher.pyw) inside this Startup folder.
