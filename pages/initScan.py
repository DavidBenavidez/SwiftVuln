# Import tkinter packages
import Tkinter as tk
from PIL import Image, ImageTk
from ui import create_rounded_rectangle, colors


# Import system Packages
import sys
sys.path.append("..")

import pages

class InitScan(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg=colors.DWHITE)
        self.root = root   
        self._loadView()
    
    def toggleSubnet(self, event=None):
        self.root.scan_type = "Subnet"
        self.root.changeScreen(pages.ConfigScan)
         
    def toggleOne(self, event=None):
        self.root.scan_type = "One"
        self.root.changeScreen(pages.ConfigScan)
    
    def toggleBack(self, event=None):
        self.root.changeScreen(pages.Scan)
        
    def _loadView(self):
        logo = tk.PhotoImage(file='assets/buttons/logo_blue.png')
        subnet_scan = tk.PhotoImage(file='assets/buttons/subnet_scan.png')
        subnet_scan_hover = tk.PhotoImage(file='assets/buttons/subnet_scan_hover.png')
        one = tk.PhotoImage(file='assets/buttons/one.png')
        one_hover = tk.PhotoImage(file='assets/buttons/one_hover.png')
        back = tk.PhotoImage(file='assets/buttons/back.png')
        back_hover = tk.PhotoImage(file='assets/buttons/back_hover.png')
        
        self.logo = logo
        self.subnet_scan = subnet_scan
        self.subnet_scan_hover = subnet_scan_hover
        self.one = one
        self.one_hover = one_hover
        self.back = back
        self.back_hover = back_hover

        self.create_image(680, 370, image=self.subnet_scan, anchor=tk.E, tags="SUBNET_SCAN", activeimage=self.subnet_scan_hover)
        self.create_image(680, 220, image=self.one, anchor=tk.E, tags="ONE_SCAN", activeimage=self.one_hover)
        self.create_image(180, 100, image=self.back, anchor=tk.E, tags="BACK", activeimage=self.back_hover)
        self.create_image(900, 100, image=self.logo, anchor=tk.E)
        
        self.tag_bind('SUBNET_SCAN', '<ButtonPress-1>', self.toggleSubnet)
        self.tag_bind('ONE_SCAN', '<ButtonPress-1>', self.toggleOne)
        self.tag_bind('BACK', '<ButtonPress-1>', self.toggleBack)