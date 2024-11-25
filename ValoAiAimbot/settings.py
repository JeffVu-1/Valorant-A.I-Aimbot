import pyautogui, os

def GetCurrentDirectory():
    return os.getcwd()

#A.I Settings
#---------------------------------------------------------------#
Yolov5_Path                     = f"{GetCurrentDirectory()}\\Library\\yolov5"
Yolov5_Model                    = f"{GetCurrentDirectory()}\\Library\\Models\\best.engine"
#---------------------------------------------------------------#

#Mouse Information
#---------------------------------------------------------------#
UserMouseVid                    = None       #CONSTANT VALUE
UserMousePid                    = None       #CONSTANT VALUE
UserMouseManufacturer           = None       #CONSTANT VALUE
UserMouseSerial                 = None       #CONSTANT VALUE
#---------------------------------------------------------------#

# Monitor Settings
#---------------------------------------------------------------#
Monitor_Width, Monitor_Height = pyautogui.size()

Box_Width, Box_Height = 350, 350

center_x = Monitor_Width / 2
center_y = Monitor_Height / 2

x1 = int(center_x - Box_Width / 2)
y1 = int(center_y - Box_Height / 2)
x2 = int(center_x + Box_Width / 2)
y2 = int(center_y + Box_Height / 2)

Region = (x1, y1, x2, y2)

x, y, width, height = Region

FOV_CENTER = [int((width - x) / 2), int((height - y) / 2)]
#---------------------------------------------------------------#


#User Settings
#---------------------------------------------------------------#
#Cheat Settings
AimbotToggle                    = True      #Toggle Aimbot
SilentAimToggle                 = False     #Toggle Silent Aim
FlickBotRageToggle              = False     #Toggle Flickbot Rage
AimbotRageToggle                = False     #Toggle Aimbot Rage
CircleToggle                    = False     #Toggle Circle
DotToggle                       = False     #Toggle Dot
EnemyColor                      = True     
Activation_Range                = 50    
AimbotCoolDown                  = 0.000000000000000001       #CONSTANT VALUE
FlickBotCoolDown                = 0.05                       #CONSTANT VALUE
TargetSelection                 = 0         
FovColor                        = (0, 219, 255)      #Default Set to Blue
Lower_Color = ([230, 40, 40])                        #Default Set to RED
Upper_Color = ([255, 90, 104])                       #Default Set to RED

#Settings - One
Aimbot_KeyOne                   =  0x6      #VK_XBUTTON2
FlickBot_KeyOne                 =  0x5      #VK_XBUTTON1
#Settings - Two
Aimbot_KeyTwo                   =  0x6      #VK_XBUTTON2
FlickBot_KeyTwo                 =  0x5      #VK_XBUTTON1

#Sensitive Settings
Valorant_Sensitivity            = 0.4       #User In-Game Sensitivity
AimSpeed                        = 1*(1/Valorant_Sensitivity)
AimbotSmoothing                 = 0.5       #Higher the value Smoother, Lower the value Faster
FlickBotSmoothing               = 50      #Higher the value Smoother, Lower the value Faster
AntiRecoilValue                 = 0.5       #Anti-Recoil Strength
AntiRecoilMultiplier            = 25         #Anti-Recoil Multiplier
#---------------------------------------------------------------#

