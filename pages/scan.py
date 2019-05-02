# Import tkinter packages
import Tkinter as tk
from PIL import Image, ImageTk
from ui import create_rounded_rectangle, colors


# Import system Packages
import sys
sys.path.append("..")

import pages

class Scan(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg=colors.DWHITE)
        self.root = root   
        self._loadView()
    
    def toggleMain(self, event=None):
        self.root.changeScreen(pages.Main)
         
    def toggleDetails(self, event=None):
        self.root.changeScreen(pages.Details)
        
    def startScan(self, event=None):
        self.root.changeScreen(pages.InitScan)

    def _loadView(self):
            # CREATE NAVBAR
            create_rounded_rectangle(self, 50, 30, 300, 575, r=10, fill=colors.WHITE, outline=colors.DGRAY)
            logo = tk.PhotoImage(file='assets/buttons/logo_blue.png')
            dash = tk.PhotoImage(file='assets/buttons/dash_on.png')
            scan = tk.PhotoImage(file='assets/buttons/scan_on.png')
            details = tk.PhotoImage(file='assets/buttons/details_on.png')
            dash_off = tk.PhotoImage(file='assets/buttons/dash_off.png')
            scan_off = tk.PhotoImage(file='assets/buttons/scan_off.png')
            details_off = tk.PhotoImage(file='assets/buttons/details_off.png')

            self.logo = logo
            self.dash = dash
            self.scan = scan
            self.details = details
            self.dash_off = dash_off
            self.scan_off = scan_off
            self.details_off = details_off

            self.create_image(105, 62, image=self.logo, anchor=tk.W)

            self.create_image(145, 150, image=self.dash_off, anchor=tk.W, tags="MAIN_SWITCH", activeimage=self.dash)
            self.create_text(172, 200, text='DASHBOARD', fill=colors.GRAY)
            
            self.create_image(145, 310, image=self.scan, anchor=tk.W)
            self.create_text(172, 350, text='SCAN', fill=colors.DGRAY)
            
            self.create_image(145, 470, image=self.details_off, anchor=tk.W, tags="DETAILS_SWITCH", activeimage=self.details)
            self.create_text(172, 520, text='DETAILS', fill=colors.GRAY)
            
            self.tag_bind('MAIN_SWITCH','<ButtonPress-1>', self.toggleMain)
            self.tag_bind('DETAILS_SWITCH','<ButtonPress-1>', self.toggleDetails)
            #########################################################

            start_scan = tk.PhotoImage(file='assets/buttons/start_scan.png')
            start_scan_hover = tk.PhotoImage(file='assets/buttons/start_scan_hover.png')
            self.start_scan = start_scan
            self.start_scan_hover = start_scan_hover
            self.create_image(880, 300, image=self.start_scan, anchor=tk.E, tags="START_SCAN", activeimage=self.start_scan_hover)
            
            self.tag_bind('START_SCAN', '<ButtonPress-1>', self.startScan)