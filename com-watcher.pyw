import sys
import struct
import io
import subprocess
import threading
import time
import win32api
import win32gui
import win32con
from PIL import Image  # pystray gebruikt lichte Image wrapper
import pystray
from pystray import MenuItem as item
import serial.tools.list_ports

icon_instance = None
known_ports = {}

def create_raw_com_image():
    """Genereert een 32x32 blauwe bitmap met de tekst 'COM' zonder zware dependencies."""
    width, height = 32, 32
    # 5x7 bitmap font voor de letters 'C', 'O', 'M'
    font_5x7 = {
        'C': [
            0b01110,
            0b10001,
            0b10000,
            0b10000,
            0b10000,
            0b10001,
            0b01110
        ],
        'O': [
            0b01110,
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b10001,
            0b01110
        ],
        'M': [
            0b10001,
            0b11011,
            0b10101,
            0b10101,
            0b10001,
            0b10001,
            0b10001
        ]
    }

    # Pixel buffer (32x32 RGBA)
    pixels = bytearray(width * height * 4)

    def set_pixel(x, y, r, g, b, a=255):
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 4
            pixels[idx:idx+4] = bytes([r, g, b, a])

    # 1. Blauwe afgeronde achtergrond tekenen
    for y in range(height):
        for x in range(width):
            # Hoekjes afronden
            if (x < 3 and y < 3 and (x-3)**2 + (y-3)**2 > 9) or \
               (x > 28 and y < 3 and (x-28)**2 + (y-3)**2 > 9) or \
               (x < 3 and y > 28 and (x-3)**2 + (y-28)**2 > 9) or \
               (x > 28 and y > 28 and (x-28)**2 + (y-28)**2 > 9):
                continue
            set_pixel(x, y, 30, 144, 255, 255)

    # 2. Witte letters 'C', 'O', 'M' intekenen
    letters = ['C', 'O', 'M']
    start_x = 6
    start_y = 12

    for letter_idx, char in enumerate(letters):
        char_matrix = font_5x7[char]
        offset_x = start_x + (letter_idx * 7)
        for row_idx, row in enumerate(char_matrix):
            for col_idx in range(5):
                if (row >> (4 - col_idx)) & 1:
                    set_pixel(offset_x + col_idx, start_y + row_idx, 255, 255, 255, 255)

    return Image.frombytes("RGBA", (width, height), bytes(pixels))

def fetch_ports():
    ports = {}
    for p in serial.tools.list_ports.comports():
        vid_pid = f"{p.vid:04X}:{p.pid:04X}" if (p.vid and p.pid) else "N/A"
        ports[p.device] = {
            "desc": p.description or "Onbekend",
            "manuf": p.manufacturer or "Onbekend",
            "vid_pid": vid_pid,
            "serial": p.serial_number or "N/A",
            "hwid": p.hwid or "N/A"
        }
    return ports

def build_menu():
    global known_ports
    menu_items = []

    if not known_ports:
        menu_items.append(item("Geen actieve COM-poorten", None, enabled=False))
    else:
        for port_name in sorted(known_ports.keys()):
            info = known_ports[port_name]
            details = pystray.Menu(
                item(f"Poort: {port_name}", None, enabled=False),
                item(f"Beschrijving: {info['desc']}", None, enabled=False),
                item(f"Fabrikant: {info['manuf']}", None, enabled=False),
                item(f"VID:PID: {info['vid_pid']}", None, enabled=False),
                item(f"Serienummer: {info['serial']}", None, enabled=False),
                item(f"HWID: {info['hwid']}", None, enabled=False)
            )
            label = f"{port_name} ({info['desc']})"
            menu_items.append(item(label, details))

    menu_items.append(pystray.Menu.SEPARATOR)
    menu_items.append(item("Apparaatbeheer openen", lambda *args: subprocess.Popen(["devmgmt.msc"], shell=True)))
    menu_items.append(item("Afsluiten", on_quit))
    return pystray.Menu(*menu_items)

def update_ui_state():
    global icon_instance, known_ports
    if not icon_instance:
        return

    if known_ports:
        lines = [f"{name}: {info['desc']}" for name, info in known_ports.items()]
        icon_instance.title = ("Aanwezige COM-poorten:\n" + "\n".join(lines))[:127]
    else:
        icon_instance.title = "Geen COM-poorten aangesloten"

    icon_instance.menu = build_menu()
    try:
        icon_instance.update_menu()
    except Exception:
        pass

def show_popup(port_name, description):
    global icon_instance
    if icon_instance:
        try:
            icon_instance.notify(
                title=f"Nieuwe Poort: {port_name}",
                message=f"{description}"
            )
        except Exception:
            pass

def handle_device_change():
    global known_ports
    current_ports = {}
    new_devices = set()

    for _ in range(6):
        time.sleep(0.25)
        current_ports = fetch_ports()
        new_devices = set(current_ports.keys()) - set(known_ports.keys())
        if new_devices or (len(current_ports) < len(known_ports)):
            break

    if new_devices:
        for p in new_devices:
            desc = current_ports[p]["desc"]
            show_popup(p, desc)

    known_ports = current_ports
    update_ui_state()

def create_hidden_window():
    DBT_DEVICEARRIVAL = 0x8000
    DBT_DEVICEREMOVECOMPLETE = 0x8004

    def wndproc(hwnd, msg, wparam, lparam):
        if msg == win32con.WM_DEVICECHANGE:
            if wparam in (DBT_DEVICEARRIVAL, DBT_DEVICEREMOVECOMPLETE):
                threading.Thread(target=handle_device_change, daemon=True).start()
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = wndproc
    wc.lpszClassName = "COMWatcherDeviceListener"
    wc.hInstance = win32api.GetModuleHandle(None)

    class_atom = win32gui.RegisterClass(wc)
    hwnd = win32gui.CreateWindow(
        class_atom, "COMWatcherDeviceListenerWindow", 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None
    )

    win32gui.PumpMessages()

def on_quit(icon, item):
    icon.stop()
    sys.exit(0)

def main():
    global icon_instance, known_ports
    
    known_ports = fetch_ports()
    icon_img = create_raw_com_image()

    icon_instance = pystray.Icon(
        name="COM_Watcher",
        icon=icon_img,
        title="COM Poort Monitor",
        menu=build_menu()
    )
    
    update_ui_state()

    listener_thread = threading.Thread(target=create_hidden_window, daemon=True)
    listener_thread.start()

    icon_instance.run()

if __name__ == "__main__":
    main()
