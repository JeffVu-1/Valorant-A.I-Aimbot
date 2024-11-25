import ctypes
import os
import random
import string
import threading
import time
from ctypes import windll
import dearpygui.dearpygui as dpg
from colorama import Fore
import overlay
import settings as Settings
from instruct import MouseInstruct, DeviceNotFoundError

main_callback = None

all_keys = [
    0x01,0x05, 0x06, 0x08, 0x09, 0x0C, 0x0D, 0x10, 0x11, 0x12, 0x13, 0x1B, 0x14, 0x14, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
    0x28, 0x29, 0x2A, 0x2B, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x41, 0x42, 0x43,
    0x44, 0x45, 0x46, 0x47, 0x48, 0x49, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57,
    0x58, 0x59, 0x5A, 0x60, 0x61, 0x62, 0x63, 0x64, 0x65,
    0x66, 0x67, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F, 0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79,
    0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x7F, 0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87, 0x90, 0x91, 0xA0, 0xA1, 0xA2, 0xA3,
    0xA4, 0xA5, 0x5B, 0x5C, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA,
    0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5, 0xB6, 0xB7, 0xF6, 0xF7, 0xF8, 0xFA, 0xFB, 0xFE,
    0xBB, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF, 0xC0, 0xBA, 0xDB, 0xDC, 0xDD, 0xDE, 0xC0, 0x26, 0x28, 0x25, 0x27, 0x02, 0x03, 0x04
]
all_key_names = {
    0x01: 'Left Mouse',             0x1: 'Left Mouse',                 0x02: 'Right Mouse',           0x2: 'Right Mouse',
    0x03: 'Control-break Processing', 0x3: 'Control-break Processing', 0x04: 'Middle Mouse Button',   0x4: 'Middle Mouse Button',
    0x05: 'Mouse Button 4',         0x5: 'Mouse Button 4',       0x06: 'Mouse Button 5',       0x6: 'Mouse Button 5',
    0x08: 'Backspace',              0x09: 'Tab',                0x0C: 'Clear',               0x0D: 'Enter',
    0x10: 'Shift',                  0x11: 'Ctrl',               0x12: 'Alt',                0x13: 'Pause',
    0x1B: 'Escape',                 0x14: 'Caps Lock',          0x20: 'Space',              0x21: 'Page Up',
    0x22: 'Page Down',              0x23: 'End',                0x24: 'Home',               0x25: 'Left Arrow',
    0x26: 'Up Arrow',               0x27: 'Right Arrow',         0x28: 'Down Arrow',        0x29: 'Select',
    0x2A: 'Print',                  0x2B: 'Execute',            0x2C: 'Print Screen',      0x2D: 'Insert',
    0x2E: 'Delete',                 0x2F: 'Help',               0x30: '0',                  0x31: '1',
    0x32: '2',                      0x33: '3',                  0x34: '4',                  0x35: '5',
    0x36: '6',                      0x37: '7',                  0x38: '8',                  0x39: '9',
    0x41: 'A',                      0x42: 'B',                  0x43: 'C',                  0x44: 'D',
    0x45: 'E',                      0x46: 'F',                  0x47: 'G',                  0x48: 'H',
    0x49: 'I',                      0x4A: 'J',                  0x4B: 'K',                  0x4C: 'L',
    0x4D: 'M',                      0x4E: 'N',                  0x4F: 'O',                  0x50: 'P',
    0x51: 'Q',                      0x52: 'R',                  0x53: 'S',                  0x54: 'T',
    0x55: 'U',                      0x56: 'V',                  0x57: 'W',                  0x58: 'X',
    0x59: 'Y',                      0x5A: 'Z',                  0x60: 'Numpad 0',           0x61: 'Numpad 1',
    0x62: 'Numpad 2',               0x63: 'Numpad 3',           0x64: 'Numpad 4',           0x65: 'Numpad 5',
    0x66: 'Numpad 6',               0x67: 'Numpad 7',           0x68: 'Numpad 8',           0x69: 'Numpad 9',
    0x6A: 'Multiply Key',           0x6B: 'Add Key',            0x6C: 'Separator Key',      0x6D: 'Subtract Key',
    0x6E: 'Decimal Key',            0x6F: 'Divide Key',         0x70: 'F1',                 0x71: 'F2',
    0x72: 'F3',                     0x73: 'F4',                 0x74: 'F5',                 0x75: 'F6',
    0x76: 'F7',                     0x77: 'F8',                 0x78: 'F9',                 0x79: 'F10',
    0x7A: 'F11',                    0x7B: 'F12',                0x7C: 'F13',                0x7D: 'F14',
    0x7E: 'F15',                    0x7F: 'F16',                0x80: 'F17',                0x81: 'F18',
    0x82: 'F19',                    0x83: 'F20',                0x84: 'F21',                0x85: 'F22',
    0x86: 'F23',                    0x87: 'F24',                0x90: 'Num Lock',           0x91: 'Scroll Lock',
    0xA0: 'Left Shift',             0xA1: 'Right Shift',        0xA2: 'Left Ctrl',          0xA3: 'Right Ctrl',
    0xA4: 'Left Alt',               0xA5: 'Right Alt',          0x5B: 'Left Windows',       0x5C: 'Right Windows',
    0xA6: 'Browser Back',           0xA7: 'Browser Forward',    0xA8: 'Browser Refresh',    0xA9: 'Browser Stop',
    0xAA: 'Browser Search',         0xAB: 'Browser Favorites',  0xAC: 'Browser Start And Home', 0xAD: 'Volume Mute',
    0xAE: 'Volume Down',            0xAF: 'Volume Up',          0xB0: 'Next Track',        0xB1: 'Previous Track',
    0xB2: 'Stop Media',             0xB3: 'Play/Pause Media',   0xB4: 'Start Mail',        0xB5: 'Select Media',
    0xB6: 'Start Application 1',    0xB7: 'Start Application 2', 0xF6: 'Attn Key',          0xF7: 'Crsel Key',
    0xF8: 'Exsel Key',              0xFA: 'Play Key',           0xFB: 'Zoom Key',          0xFE: 'Clear Key',
    0xBB: '=',                      0xBC: ',',                  0xBD: '-',                0xBE: '.',
    0xBF: '/',                      0xC0: '`',                  0xBA: ';',                0xDB: '[',
    0xDC: '\\',                     0xDD: ']',                 0xDE: "'",                0x26: 'Up Arrow',
    0x28: 'Down Arrow',             0x25: 'Left Arrow',          0x27: 'Right Arrow'
}


#Login Screen Function
#---------------------------------------------------------------#
def submit_login():
    global key
    key = str(dpg.get_value("LoginTextBox"))
    if key == "":
        pass
    else:  
        print("Key Submitted: ", key)
        with open(os.path.join(GetCurrentDirectory(), "Library", "license.txt"), "w") as f:
            f.write(key)
        if main_callback:
            main_callback()

def load_previous_key():
    if os.path.exists(os.path.join(GetCurrentDirectory(), "Library", "license.txt")):
        with open(os.path.join(GetCurrentDirectory(), "Library", "license.txt"), "r") as f:
            key = f.readline()
            dpg.set_value("LoginTextBox", key)

#---------------------------------------------------------------#

#General Functions
#---------------------------------------------------------------#
def random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

def Main_CallBack(callback):
    global main_callback
    main_callback = callback

def GetKeyState(v_key: int) -> bool:
    return bool(windll.user32.GetKeyState(v_key) & 0x80)

def cooldown(cooldown_bool, wait):
    time.sleep(wait)
    cooldown_bool[0] = True

def GetCurrentDirectory():
    return os.getcwd()

def ChangeFovCircleColor(sender, app_data):
    Settings.FovColor = (app_data[0]*255, app_data[1]*255, app_data[2]*255)
    overlay.window.ChangeColor(sender, app_data)
#---------------------------------------------------------------#

#Mouse Functions / Game Boot Functions
#---------------------------------------------------------------#
def ReadMouseTXT():
    with open(os.path.join(GetCurrentDirectory(),"Library", "Mouse.txt"), "r") as file:
        for line in file:
            if "vid" in line.lower():
                Settings.UserMouseVid = int(line.split("=")[1].strip(), 16)
            if "pid" in line.lower():
                Settings.UserMousePid = int(line.split("=")[1].strip(), 16)
            if "manufacturer_string" in line.lower():
                Settings.UserMouseManufacturer = line.split("=")[1].strip()
            if "serial" in line.lower():
                Settings.UserMouseSerial = line.split("=")[1].strip()	

def ObtainMouse():
    try:
        Mouse = MouseInstruct.getMouse(Settings.UserMouseVid, Settings.UserMousePid, Settings.UserMouseManufacturer, Settings.UserMouseSerial)
        print(Fore.LIGHTGREEN_EX + "[+] Mouse found [+]\n")
    except DeviceNotFoundError as e:
        input(Fore.RED + "Mouse Not Found, Press Enter to Exit\n")
    return Mouse, True
#---------------------------------------------------------------#

# UPDATE KEYBIND FUNCTIONS / Sensitivity Functions
#---------------------------------------------------------------#
def AimbotPrimaryKeyUpdater(sender):
    dpg.configure_item("AimbotKey", label="<Listening>")
    def KeyListener():
        global key_selected, New_Label
        key_selected = False
        while True:
            if key_selected == False:
                for key in all_keys:
                    if GetKeyState(key):
                        GrabNameFromKeyCode = all_key_names.get(key, f"Key Code: {key}")
                        New_Label = f"{GrabNameFromKeyCode}"
                        dpg.configure_item("AimbotKey", label=New_Label)
                        key_selected = True ; Settings.Aimbot_KeyOne = key
                        return
                    
    threading.Thread(target=KeyListener).start()

def FlickBotPrimaryKeyUpdater(sender):
    dpg.configure_item("FlickBotKey", label="<Listening>")
    def KeyListener():
        global key_selected, New_Label
        key_selected = False
        while True:
            if key_selected == False:
                for key in all_keys:
                    if GetKeyState(key):
                        GrabNameFromKeyCode = all_key_names.get(key, f"Key Code: {key}")
                        New_Label = f"{GrabNameFromKeyCode}"
                        dpg.configure_item("FlickBotKey", label=New_Label)
                        key_selected = True ; Settings.FlickBot_KeyOne = key
                        return
    threading.Thread(target=KeyListener).start()

def UpdateSensitivity(sender):
    try:
        Settings.Valorant_Sensitivity = float(dpg.get_value("ValorantSensitivity"))
        Settings.AimSpeed = 1 *(1/Settings.Valorant_Sensitivity)
        print(f"Valorant Sensitivity: {Settings.Valorant_Sensitivity}")
        print(f"Aimspeed Sensitivity: {Settings.AimSpeed}")
    except ValueError:
        dpg.configure_item("ValorantSensitivity", default_value=Settings.Valorant_Sensitivity)
#---------------------------------------------------------------#


# Toggle Functions
#---------------------------------------------------------------#
def AimbotRageToggle(sender):
    if dpg.get_value(sender):
        Settings.AimbotRageToggle = True
    else:
        Settings.AimbotRageToggle = False

def FlickBotRageToggle(sender):
    if dpg.get_value(sender):
        Settings.FlickBotRageToggle = True
    else:
        Settings.FlickBotRageToggle = False

def SilentAimToggle(sender):
    if dpg.get_value(sender):
        Settings.SilentAimToggle = True
    else:
        Settings.SilentAimToggle = False
#---------------------------------------------------------------#


# SLIDER FUNCTIONS
#---------------------------------------------------------------#
def UpdateFovRange(sender, app_data, user_data):
    window = user_data
    Settings.Activation_Range = dpg.get_value(sender) 
    window.ChangeFovCircle(sender, app_data)
    
def UpdateAimbotSmoothing():
    Settings.AimbotSmoothing = (dpg.get_value("AimbotSmoothingSlider") / 10)

def UpdateFlickBotSmoothing():
    Settings.FlickBotSmoothing = int((dpg.get_value("FlickBotSmoothingSlider")))

def UpdateAntiRecoilValue():
    Settings.AntiRecoilMultiplier = (dpg.get_value("AntiRecoilSlider") / 2)
#---------------------------------------------------------------#


# ComboBox Functions
#---------------------------------------------------------------#
def SelectOutlineColorComboBox(sender):                             
    OutLineSelection = dpg.get_value("EnemyOutlineColor")
    if OutLineSelection == "Outline - Red":
        Settings.EnemyColor = True
        Settings.Lower_Color = ([230, 40, 40])
        Settings.Upper_Color = ([255, 90, 104])
    elif OutLineSelection == "Outline - Yellow":
        Settings.EnemyColor = True
        Settings.Lower_Color = ([200, 200, 14])
        Settings.Upper_Color = ([255, 255, 100])
    elif OutLineSelection == "Outline - Purple":
        Settings.EnemyColor = True
        Settings.Lower_Color = ([160, 80, 179])
        Settings.Upper_Color = ([255, 128, 255])
    else:
        Settings.EnemyColor = False
#---------------------------------------------------------------#

# Thread
#---------------------------------------------------------------#
def Anti_Recoil_Thread():
    while True:
        while GetKeyState(0x01):
            Settings.AntiRecoilValue += 0.025 * Settings.AntiRecoilMultiplier
            time.sleep(0.0025)
        else:
            Settings.AntiRecoilValue = 0
#---------------------------------------------------------------#

# Confg Functions
#---------------------------------------------------------------#
def ActualLoadConfigButton(sender):
    dpg.configure_item("LoadConfigMenu", show=False)
    dpg.configure_item("Settings", show=True)
    selected_item = dpg.get_value("Config_List")
    if selected_item:
        config_file_path = os.path.join(GetCurrentDirectory(), "Library", "Configuration", selected_item)
        if os.path.exists(config_file_path):
            with open(config_file_path, 'r') as config_file:
                config_data = config_file.readlines()
                for line in config_data:
                    key, value = map(str.strip, line.split('='))
                    if key == "Valorant_Sensitivity":
                        Settings.Valorant_Sensitivity = float(value)
                        dpg.configure_item("ValorantSensitivity", default_value="Valorant Sensitivity Set to " + str(Settings.Valorant_Sensitivity))
                        Settings.AimSpeed = 1 *(1/Settings.Valorant_Sensitivity)
                        #print(f"Valorant Sensitivity: {Settings.Valorant_Sensitivity}")
                    elif key == "AimbotFovRange":
                        Settings.Activation_Range = Settings.Activation_Range = int(float(value))
                        dpg.configure_item("Fov", default_value=int(Settings.Activation_Range))
                    elif key == "AimbotSmoothing":
                        Settings.AimbotSmoothing = float(value)/10
                        dpg.configure_item("AimbotSmoothingSlider", default_value=(Settings.AimbotSmoothing*10))
                    elif key == "AntiRecoilMultiplier":
                        Settings.AntiRecoilMultiplier = float(value)
                        dpg.configure_item("AntiRecoilSlider", default_value=Settings.AntiRecoilMultiplier*2)
                    elif key == "FlickBotSteps":
                        Settings.FlickBotSteps = int(value)
                        dpg.configure_item("FlickBotSmoothingSlider", default_value=Settings.FlickBotSteps)
                    elif key == "Aimbot_KeyOne":
                        Settings.Aimbot_KeyOne = int(value)
                        dpg.configure_item("AimbotKey", label=f"{all_key_names.get(Settings.Aimbot_KeyOne, f'Key Code: {Settings.Aimbot_KeyOne}')}")
                    elif key == "FlickBot_KeyOne":
                        Settings.FlickBot_KeyOne = int(value)
                        dpg.configure_item("FlickBotKey", label=f"{all_key_names.get(Settings.FlickBot_KeyOne, f'Key Code: {Settings.FlickBot_KeyOne}')}")
                    elif key == "EnemyColor":
                        Settings.EnemyColor = bool(value)
                    elif key == "Lower_Color":
                        Settings.Lower_Color = eval(value)
                    elif key == "Upper_Color":
                        Settings.Upper_Color = eval(value)
                        if Settings.Upper_Color == [255, 90, 104]:
                            dpg.configure_item("EnemyOutlineColor", default_value="Outline - Red")
                        elif Settings.Upper_Color == [255, 255, 100]:
                            dpg.configure_item("EnemyOutlineColor", default_value="Outline - Yellow")
                        elif Settings.Upper_Color == [255, 128, 255]:
                            dpg.configure_item("EnemyOutlineColor", default_value="Outline - Purple")
                    elif key == "FlickBotRageToggle":
                        if value == "False":
                            Settings.FlickBotRageToggle = False
                            dpg.set_value("FlickBotRage", False)
                        elif value == "True":
                            Settings.FlickBotRageToggle = True
                            dpg.set_value("FlickBotRage", True)     
                    elif key == "AimbotRageToggle":
                        if value == "False":
                            Settings.AimbotRageToggle = False
                            dpg.set_value("AimbotRage", False)
                        elif value == "True":
                            Settings.AimbotRageToggle = True
                            dpg.set_value("AimbotRage", True)               
                    elif key == "SilentAimToggle":
                        if value == "False":
                            Settings.SilentAimToggle = False
                            dpg.set_value("SilentAim", False)
                        elif value == "True":
                            Settings.SilentAimToggle = True
                            dpg.set_value("SilentAim", True)
                    elif key == "FovColor":
                        Settings.FovColor = eval(value)
                        dpg.configure_item("FovColorWheel", default_value=Settings.FovColor)
                        overlay.window.ChangeColor(sender, (Settings.FovColor[0]/255, Settings.FovColor[1]/255, Settings.FovColor[2]/255))
                    elif key == "CircleToggle":
                        if value == "False":
                            overlay.window.Enable = False
                            dpg.set_value("Circle", False)
                        elif value == "True":
                            Settings.CircleToggle = True
                            overlay.window.Enable = True
                            overlay.window.ChangeFovCircle(sender, Settings.Activation_Range)
                            dpg.set_value("Circle", True)
                    elif key == "DotToggle":
                        if value == "False":
                            overlay.window.draw_center_dot = False
                            dpg.set_value("Dot", False)
                        elif value == "True":
                            Settings.DotToggle = True
                            overlay.window.draw_center_dot = True
                            overlay.window.ChangeFovCircle(sender, Settings.Activation_Range)
                            dpg.set_value("Dot", True)

def ActualSaveConfigButton():
    config_name = dpg.get_value("SaveConfigTextBox")
    dpg.configure_item("SaveConfigMenu", show=False)
    dpg.configure_item("Settings", show=True)    
    if config_name:
        config_file_path = os.path.join(GetCurrentDirectory(),"Library","Configuration", f"{config_name}.txt")
        with open(config_file_path, 'w') as config_file:
            config_file.write(f'Valorant_Sensitivity={Settings.Valorant_Sensitivity}\n')
            config_file.write(f'AimbotFovRange={Settings.Activation_Range}\n')
            config_file.write(f'AimbotSmoothing={int(Settings.AimbotSmoothing*10)}\n')
            config_file.write(f'AntiRecoilMultiplier={Settings.AntiRecoilMultiplier}\n')
            config_file.write(f'FlickBotSteps={Settings.FlickBotSmoothing}\n')
            config_file.write(f'Aimbot_KeyOne={Settings.Aimbot_KeyOne}\n')
            config_file.write(f'FlickBot_KeyOne={Settings.FlickBot_KeyOne}\n')
            config_file.write(f'SilentAimToggle={Settings.SilentAimToggle}\n')
            config_file.write(f'EnemyColor={Settings.EnemyColor}\n')
            config_file.write(f'Lower_Color={Settings.Lower_Color}\n')
            config_file.write(f'Upper_Color={Settings.Upper_Color}\n')
            config_file.write(f'FovColor={Settings.FovColor}\n')
            config_file.write(f'FlickBotRageToggle={Settings.FlickBotRageToggle}\n')
            config_file.write(f'AimbotRageToggle={Settings.AimbotRageToggle}\n')
            config_file.write(f'CircleToggle={Settings.CircleToggle}\n')
            config_file.write(f'DotToggle={Settings.DotToggle}\n')


