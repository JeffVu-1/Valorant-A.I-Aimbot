import threading
from time import sleep as Sleep
import settings as Settings
from functions import GetKeyState, cooldown

def CalculateBezierPoint(t, p0, p1, p2):
    u = (1 - t)
    tt = (t * t)
    uu = (u * u)

    x = int(uu * p0[0] + 2 * u * t * p1[0] + tt * p2[0])
    y = int(uu * p0[1] + 2 * u * t * p1[1] + tt * p2[1])

    return (x, y)

def move_mouse_smoothly(starting_point, firstcontrolpoint, target, steps, Mouse):
    for i in range(steps):
        t = i / steps
        bezierPointX, bezierPointY = CalculateBezierPoint(t, starting_point, firstcontrolpoint, target)
        
        if abs(bezierPointX - starting_point[0]) > 127:
            while abs(bezierPointX - starting_point[0]) > 127:
                step_bezierPointX = 127 if bezierPointX > starting_point[0] else -127
                Mouse.move(int(step_bezierPointX), 0)
                bezierPointX -= step_bezierPointX
        
        if abs(bezierPointY - starting_point[1]) > 127:
            while abs(bezierPointY - starting_point[1]) > 127:
                step_bezierPointY = 127 if bezierPointY > starting_point[1] else -127
                Mouse.move(0, int(step_bezierPointY))
                bezierPointY -= step_bezierPointY
        
        move_x = int(bezierPointX - starting_point[0])
        move_y = int(bezierPointY - starting_point[1])
        Mouse.move(move_x, move_y)
        
        starting_point = (bezierPointX, bezierPointY) 

#Aimbot Tracking 
def AimbotTrackingLegit(head_center_list, FOV_CENTER, ymax, ymin, Mouse):

    SmoothingAmount = Settings.AimbotSmoothing
    Aimspeed = Settings.AimSpeed
    AimSpeedAgain = Aimspeed / SmoothingAmount

    xdif = (head_center_list[0] - FOV_CENTER[0]) * AimSpeedAgain
    ydif = ((head_center_list[1] - FOV_CENTER[1]) + Settings.AntiRecoilValue) * AimSpeedAgain 

    if abs(xdif) > 127:
        while abs(xdif) > 127:
            step_xdif = 127 if xdif > 0 else -127
            Mouse.move(int(step_xdif), 0)
            xdif -= step_xdif

    if abs(ydif) > 127:
        while abs(ydif) > 127:
            step_ydif = 127 if ydif > 0 else -127
            Mouse.move(0, int(step_ydif))
            ydif -= step_ydif

    Mouse.move(int(xdif), int(ydif))
    
def AimbotTrackingRage(head_center_list, FOV_CENTER, ymax, ymin, Mouse):

    xdif = (head_center_list[0] - FOV_CENTER[0]) * Settings.AimSpeed
    ydif = (head_center_list[1] - FOV_CENTER[1]) * Settings.AimSpeed

    
    if abs(xdif) > 127:
        while abs(xdif) > 127:
            step_xdif = 127 if xdif > 0 else -127
            Mouse.move(int(step_xdif), 0)
            xdif -= step_xdif


    if abs(ydif) > 127:
        while abs(ydif) > 127:
            step_ydif = 127 if ydif > 0 else -127
            Mouse.move(0, int(step_ydif))
            ydif -= step_ydif

    Mouse.move(int(xdif), int(ydif) + Settings.AntiRecoilValue)
    
    Sleep(0.02) 

#FlickBot
def FlickBot(head_center_list, FOV_CENTER, ymax, ymin, Mouse, send_next, FlickBotCoolDown):
    if  GetKeyState(0x02) == True:  
        xdif = (head_center_list[0] - FOV_CENTER[0])*Settings.AimSpeed*0.9
        ydif = (head_center_list[1] - FOV_CENTER[1])*Settings.AimSpeed*0.9                                       
    else:                           
        xdif = (head_center_list[0] - FOV_CENTER[0])*Settings.AimSpeed*1.05
        ydif = (head_center_list[1] - FOV_CENTER[1])*Settings.AimSpeed*1.05  

    if abs(xdif) > 127:
        while abs(xdif) > 127:
            step_xdif = 127 if xdif > 0 else -127
            Mouse.move(int(step_xdif), 0) 
            xdif -= step_xdif
    if abs(ydif) > 127:
        while abs(ydif) > 127:
            step_ydif = 127 if ydif > 0 else -127
            Mouse.move(0, int(step_ydif))
            ydif -= step_ydif

    Mouse.move(int(xdif), int(ydif))
    Mouse.click()
        
    send_next[0] = False
    thread = threading.Thread(target=cooldown, args=(send_next,FlickBotCoolDown))
    thread.start()


def FlickBotLegit(head_center_list, FOV_CENTER, ymax, ymin, Mouse, send_next, FlickBotCoolDown):
    if  GetKeyState(0x02) == True:  
        xdif = (head_center_list[0] - FOV_CENTER[0])*Settings.AimSpeed*0.9
        ydif = (head_center_list[1] - FOV_CENTER[1])*Settings.AimSpeed*0.9                                       
    else:                           
        xdif = (head_center_list[0] - FOV_CENTER[0])*Settings.AimSpeed*1.05
        ydif = (head_center_list[1] - FOV_CENTER[1])*Settings.AimSpeed*1.05  

    steps = Settings.FlickBotSmoothing

    x_step = xdif / steps
    y_step = ydif / steps

    x_accum = 0.0
    y_accum = 0.0

    for _ in range(steps):
        x_accum += x_step
        y_accum += y_step

        Mouse.move(int(round(x_accum)), int(round(y_accum)))

        x_accum -= int(round(x_accum))
        y_accum -= int(round(y_accum))

    Mouse.click()
    Sleep(FlickBotCoolDown)


def SilentAim(head_center_list, FOV_CENTER, ymax, ymin, Mouse, send_next, FlickBotCoolDown):
    if GetKeyState(0x02) == True:
        xdif = (head_center_list[0] - FOV_CENTER[0])*Settings.AimSpeed*0.9
        ydif = (head_center_list[1] - FOV_CENTER[1])*Settings.AimSpeed*0.9
        ReverseX = -xdif
        ReverseY = -ydif
    else:
        xdif = (head_center_list[0] - FOV_CENTER[0])*Settings.AimSpeed*1.05
        ydif = (head_center_list[1] - FOV_CENTER[1])*Settings.AimSpeed*1.05
        ReverseX = -xdif
        ReverseY = -ydif

    ReverseX = -xdif
    ReverseY = -ydif

    if abs(xdif) > 127:
        while abs(xdif) > 127:
            step_xdif = 127 if xdif > 0 else -127
            Mouse.move(int(step_xdif), 0) 
            xdif -= step_xdif
    if abs(ydif) > 127:
        while abs(ydif) > 127:
            step_ydif = 127 if ydif > 0 else -127
            Mouse.move(0, int(step_ydif)) 
            ydif -= step_ydif
    Mouse.move(int(xdif), int(ydif))
    Sleep(1e-44)
    Mouse.click()
    Sleep(1e-44)
    if abs(ReverseX) > 127:
        while abs(ReverseX) > 127:
            step_reverse_x = 127 if ReverseX > 0 else -127
            Mouse.move(int(step_reverse_x), 0) 
            ReverseX -= step_reverse_x
    if abs(ReverseY) > 127:
        while abs(ReverseY) > 127:
            step_reverse_y = 127 if ReverseY > 0 else -127
            Mouse.move(0, int(step_reverse_y))  
            ReverseY -= step_reverse_y
    Mouse.move(int(ReverseX), int(ReverseY))

    send_next[0] = False
    thread = threading.Thread(target=cooldown, args=(send_next,FlickBotCoolDown))
    thread.start()
