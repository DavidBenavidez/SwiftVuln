import tkinter as tk 

from PIL import Image, ImageTk
from utils import _getFont, colors
from ui import create_rounded_rectangle

import menu

class Scan(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg=colors.DWHITE)

        self.root = root   
        self._loadView()
    
    def toggleMain(self, event=None):
        print("Main!")
        self.root.changeScreen(menu.Main)
         
    def toggleDetails(self, event=None):
        print("Details!")
        self.root.changeScreen(menu.Details)
        
    def _loadView(self):
            create_rounded_rectangle(self, 175, 320, 825, 400, r=10, fill=colors.LBLUE, outline=colors.BLUE)
            create_rounded_rectangle(self, 50, 30, 300, 575, r=10, fill=colors.WHITE, outline=colors.DGRAY)
            dash = tk.PhotoImage(file='assets/buttons/dash_off.png')
            scan = tk.PhotoImage(file='assets/buttons/scan_on.png')
            details = tk.PhotoImage(file='assets/buttons/details_off.png')
            
            self.dash = dash
            self.scan = scan
            self.details = details

            self.create_image(145, 120, image=self.dash, anchor=tk.W, tags="MAIN_SWITCH")
            self.create_text(172, 170, text='DASHBOARD', fill=colors.GRAY)
            
            self.create_image(145, 300, image=self.scan, anchor=tk.W)
            self.create_text(172, 350, text='SCAN', fill=colors.DGRAY)
            
            self.create_image(145, 480, image=self.details, anchor=tk.W, tags="DETAILS_SWITCH")
            self.create_text(172, 530, text='DETAILS', fill=colors.GRAY)

            self.tag_bind('MAIN_SWITCH','<ButtonPress-1>', self.toggleMain)
            self.tag_bind('DETAILS_SWITCH','<ButtonPress-1>', self.toggleDetails)