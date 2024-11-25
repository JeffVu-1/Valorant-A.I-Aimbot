import hashlib
import math
import os
import sys
import threading
from time import sleep as Sleep
import cv2
import dearpygui.dearpygui as dpg
import numpy as np
import torch
from colorama import Fore
import bettercam
import functions
import settings as Settings
from aimbot import AimbotTrackingLegit, FlickBot, SilentAim, FlickBotLegit, AimbotTrackingRage
from auth import api
from functions import GetKeyState, ReadMouseTXT, ObtainMouse, Anti_Recoil_Thread
from gui import gui
from overlay import Overlay
from settings import Region, FOV_CENTER, FlickBotCoolDown, Yolov5_Path, Yolov5_Model


send_next = [True]
camera = bettercam.create(output_idx=0, output_color="BGRA")
UpdateMouse = ReadMouseTXT()
Mouse, Status = ObtainMouse()

def main():
    #REMOVE KEY AUTH BELOW IF YOU'RE USING THIS YOURSELF
    try:
        def getchecksum():
                md5_hash = hashlib.md5()
                file = open(''.join(sys.argv), "rb")
                md5_hash.update(file.read())
                digest = md5_hash.hexdigest()
                return digest

        keyauthapp = api(
        name = "Aimbot", 
        ownerid = "5JKLmPrXy2", 
        secret = "a4d85c47e3a11a46fbc9e7dba7d8e12ef1c29b9c7b8d3f62c8c9f5a8b3e8d492", 
        version = "1.0",
        hash_to_check = getchecksum())

        key = functions.key
        keyauthapp.license(key)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    else:
        dpg.configure_item("LoginScreen", show=False)

        try:
            os.system('cls' if os.name == 'nt' else 'clear')   

            yolov5_model = torch.hub.load(Yolov5_Path, 'custom', path=Yolov5_Model, source='local', force_reload=True).eval().cuda()
            yolov5_model.maxdet = 5
            yolov5_model.apm = True
            yolov5_model.conf = 0.50
            
        except Exception as e:
            print(f"An error occurred: {e}")

        def start_main_code():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.GREEN + "Successfully Loaded - Do Not Close This Window")
            dpg.configure_item("Main", show=True)
            main()

        def main():
            while True:
                closest_part_distance = 100000
                closest_part = -1
                screenshot = camera.grab(Region)
                if screenshot is None: continue

            
                df = yolov5_model(screenshot, size=640).pandas().xyxy[0]

                for i in range(0,10):
                    try:
                        xmin = int(df.iloc[i,0])
                        ymin = int(df.iloc[i,1])
                        xmax = int(df.iloc[i,2])    
                        ymax = int(df.iloc[i,3])

                        centerX = (xmax-xmin)/2+xmin 
                        centerY = (ymax-ymin)/2+ymin

                        distance = math.dist([centerX, centerY], FOV_CENTER)
                        if Settings.EnemyColor == True:
                            part_image = screenshot[ymin - 10:ymax + 20, xmin - 10:xmax + 10] # check for color box size
                            hsv_part = cv2.cvtColor(part_image, cv2.COLOR_BGR2RGB)
                            mask = cv2.inRange(hsv_part, np.array(Settings.Lower_Color), np.array(Settings.Upper_Color))
                            kernel = np.zeros((5,5), np.uint8)
                            dilated = cv2.dilate(mask, kernel, iterations=2)  
                            color_percentage = np.count_nonzero(dilated) / (part_image.shape[0] * part_image.shape[1])

                            if int(distance) < closest_part_distance and color_percentage > 0:
                                closest_part_distance = distance
                                closest_part = i
                        else:
                            if int(distance) < closest_part_distance:
                                closest_part_distance = distance
                                closest_part = i
                    except: 
                        pass

                if closest_part != -1:
                    xmin = df.iloc[closest_part,0]
                    ymin = df.iloc[closest_part,1]
                    xmax = df.iloc[closest_part,2]
                    ymax = df.iloc[closest_part,3]

                    head_center_list = [(xmax-xmin)/2+xmin,(ymax-ymin)/2+ymin]

                    #Aimbot
                    if (GetKeyState(Settings.Aimbot_KeyOne) and closest_part_distance < Settings.Activation_Range and Settings.AimbotToggle == True):
                        if Settings.AimbotRageToggle == True:
                            AimbotTrackingRage(head_center_list, FOV_CENTER, ymax, ymin, Mouse)
                        else:
                            AimbotTrackingLegit(head_center_list, FOV_CENTER, ymax, ymin, Mouse) 
                    
                    # Flickbot
                    while (GetKeyState(Settings.FlickBot_KeyOne) and closest_part_distance < Settings.Activation_Range and send_next[0] == True and Settings.AimbotToggle == True and Settings.SilentAimToggle == False):
                        if Settings.FlickBotRageToggle == True:
                            FlickBot(head_center_list, FOV_CENTER, ymax, ymin, Mouse, send_next, FlickBotCoolDown)
                        else:
                            FlickBotLegit(head_center_list, FOV_CENTER, ymax, ymin, Mouse, send_next, FlickBotCoolDown)

                    #SilentAim
                    if (GetKeyState(Settings.FlickBot_KeyOne) and closest_part_distance < Settings.Activation_Range and send_next[0] == True and Settings.AimbotToggle == True and Settings.SilentAimToggle == True):
                        SilentAim(head_center_list, FOV_CENTER, ymax, ymin, Mouse, send_next, FlickBotCoolDown)

        threading.Thread(target=start_main_code).start()
        threading.Thread(target=Anti_Recoil_Thread).start()

if __name__ == "__main__":
    functions.Main_CallBack(main)
    threading.Thread(target=Overlay).start()
    Sleep(1)
    threading.Thread(target=gui).start()
    
  