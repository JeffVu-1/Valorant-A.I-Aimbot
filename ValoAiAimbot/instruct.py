from enum import Enum
import hid

MOUSE_LEFT = 1
MOUSE_RIGHT = 2
MOUSE_MIDDLE = 4
MOUSE_ALL = MOUSE_LEFT | MOUSE_RIGHT | MOUSE_MIDDLE

class MouseInstruct:
    def __init__(self, dev):
        self._buttons_mask = 0
        self._dev = dev
        self.move(0, 0)

    @classmethod
    def getMouse(cls, vid, pid, manufacturer_string, serial_number, ping_code=0xDF, ):
        dev = find_mouse_device(vid, pid, ping_code, manufacturer_string, serial_number)
        if not dev:
            raise DeviceNotFoundError(
                f"[-] Device Vendor ID: {hex(vid)}, Product ID: {hex(pid)} not found!"
                )
        return cls(dev)

    def _buttons(self, buttons):
        if buttons != self._buttons_mask:
            self._buttons_mask = buttons
            self.move(0, 0)

    def click(self, button = MOUSE_LEFT):
        self._buttons_mask = button
        self.move(0, 0)
        self._buttons_mask = 0
        self.move(0, 0)

    def press(self, button = MOUSE_LEFT):
        self._buttons(self._buttons_mask | button)

    def release(self, button = MOUSE_LEFT):
        self._buttons(self._buttons_mask & ~button)

    def is_pressed(self, button = MOUSE_LEFT):
        return bool(button & self._buttons_mask)

    def move(self, x, y):
        limited_x = limit_xy(x)
        limited_y = limit_xy(y)
        self._sendRawReport(self._makeReport(limited_x, limited_y))

    def _makeReport(self, x, y):
        report_data = [
                            0x01,
                            self._buttons_mask,
                            low_byte(x), high_byte(x),
                            low_byte(y), high_byte(y)
                        ]
        return report_data

    def _sendRawReport(self, report_data):
        self._dev.write(report_data)
        
class DeviceNotFoundError(Exception):
    pass

def check_ping(dev, ping_code):
    dev.write([0, ping_code])
    resp = dev.read(max_length=64, timeout_ms=100)
    
    return resp and resp[0] == ping_code

def find_mouse_device(vid, pid, ping_code, manufacturer_string, serial_number):
    for dev_info in hid.enumerate(vid, pid):
        if dev_info['manufacturer_string'] == manufacturer_string and dev_info['serial_number'] == serial_number:
            try:
                dev = hid.device()
                dev.open_path(dev_info['path'])
                
                found = check_ping(dev, ping_code)
                
                if found:
                    return dev
                else:
                    dev.close()
            except Exception as e:
                print(f"Error initializing device: {e}")
    return None


def print_descriptors(vid, pid):
    for dev_info in hid.enumerate(vid, pid):
        for key, value in dev_info.items():
            print(key, value)
    
    return None

def fetch_descriptors(serial_number="AHIDGD"):
    for dev_info in hid.enumerate():
        if dev_info['serial_number'] == serial_number:
            return dev_info["manufacturer_string"], hex(dev_info["vendor_id"])[2:], hex(dev_info["product_id"])[2:]
        
def limit_xy(xy):
    if xy < -127:
        return -127
    elif xy > 127:
        return 127
    else: return xy

def low_byte(x):
    if not isinstance(x, (int, float)):
        raise ValueError("Input must be numeric.")
    x = int(x)
    return x & 0xFF

def high_byte(x):
    if not isinstance(x, (int, float)):
        raise ValueError("Input must be numeric.")
    x = int(x)
    return (x >> 8) & 0xFF