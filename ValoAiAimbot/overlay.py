import ctypes
import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import pyautogui
import settings as Settings

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ScreenSize = pyautogui.size()
        self.screen_width = self.ScreenSize[0]
        self.screen_height = self.ScreenSize[1]
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        self.radius = 100
        self.pen_width = 1
        self.draw_center_dot = False
        self.Enable = False
        self.Qcolor = QColor(Settings.FovColor[0], Settings.FovColor[1], Settings.FovColor[2])
        
        self.setWindowTitle("Transparent Window")
        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.setAttribute(Qt.WA_TranslucentBackground, True)  
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.set_no_activate_style()

    def set_no_activate_style(self):
        hwnd = int(self.winId())  
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -20) 
        style |= 0x08000000  
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)

    def ToggleEnable(self):
        self.Enable = not self.Enable
        self.update()

    def ToggleCenterDot(self):
        self.draw_center_dot = not self.draw_center_dot
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(self.Qcolor, self.pen_width)  

        if self.Enable:
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)  
           
            circle_rect = QRect(self.center_x - self.radius, self.center_y - self.radius, 2 * self.radius, 2 * self.radius)
            painter.drawEllipse(circle_rect)

        if self.draw_center_dot:
            dot_rect = QRect(self.center_x- 1, self.center_y - 1, 2, 2)
            painter.setPen(self.Qcolor)
            painter.setBrush(self.Qcolor)
            painter.drawEllipse(dot_rect)

    def ChangeFovCircle(self, sender, app_data):
        self.radius = int(app_data)
        self.update()

    def ChangeColor(self, sender , app_data):
        rgbInt = (int(app_data[0] * 255), int(app_data[1] * 255), int(app_data[2] * 255))
        self.Qcolor.setRgb(rgbInt[0], rgbInt[1], rgbInt[2])
        self.update()
    
window = None
def Overlay():
    global window
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())
    
    