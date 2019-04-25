# Import tkinter packages
import Tkinter as tk
from PIL import Image, ImageTk
from utils import colors
from ui import create_rounded_rectangle


# Import system Packages
import menu
import sys
sys.path.append("..")

class Scan(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg=colors.DWHITE)
        self.target_entry = tk.StringVar()
        self.root = root   
        self._loadView()
    
    def toggleMain(self, event=None):
        self.root.changeScreen(menu.Main)
         
    def toggleDetails(self, event=None):
        self.root.changeScreen(menu.Details)
        
    def startScan(self, event=None):
        target_entry = (str(self.target_entry.get()))
        self.root.target_entry = target_entry
        self.root.changeScreen(menu.StartScan)

    def _loadView(self):
            # SIDE NAVBAR
            create_rounded_rectangle(self, 50, 30, 300, 575, r=10, fill=colors.WHITE, outline=colors.DGRAY)
            dash = tk.PhotoImage(file='assets/buttons/dash_on.png')
            scan = tk.PhotoImage(file='assets/buttons/scan_on.png')
            details = tk.PhotoImage(file='assets/buttons/details_on.png')
            dash_off = tk.PhotoImage(file='assets/buttons/dash_off.png')
            scan_off = tk.PhotoImage(file='assets/buttons/scan_off.png')
            details_off = tk.PhotoImage(file='assets/buttons/details_off.png')

            self.dash = dash
            self.scan = scan
            self.details = details
            self.dash_off = dash_off
            self.scan_off = scan_off
            self.details_off = details_off

            self.create_image(145, 120, image=self.dash_off, anchor=tk.W, tags="MAIN_SWITCH", activeimage=self.dash)
            self.create_text(172, 170, text='DASHBOARD', fill=colors.GRAY)
            
            self.create_image(145, 300, image=self.scan, anchor=tk.W)
            self.create_text(172, 350, text='SCAN', fill=colors.DGRAY)
            
            self.create_image(145, 480, image=self.details_off, anchor=tk.W, tags="DETAILS_SWITCH", activeimage=self.details)
            self.create_text(172, 530, text='DETAILS', fill=colors.GRAY)

            self.tag_bind('MAIN_SWITCH','<ButtonPress-1>', self.toggleMain)
            self.tag_bind('DETAILS_SWITCH','<ButtonPress-1>', self.toggleDetails)
            #########################################################
            
            # self.create_text(520, 165, font=("Lato", 15, "bold" ), text='TOP HOSTS', fill=colors.DGRAY)

            
            # inputField = tk.Entry(
            #     self,
            #     textvariable=self.target_entry,
            #     bg=colors.DGRAY,
            #     fg=colors.WHITE,
            #     highlightcolor=colors.GRAY,
            #     justify=tk.CENTER,
            #     font='Lato'
            # )
            # fieldLabel = tk.Label(
            #     self,
            #     text='Enter target',
            #     fg='Black',
            #     bg=colors.DWHITE,
            #     font='Lato'
            # )
            # fieldLabel.place(x=650, y=230, anchor='center')
            # inputField.place(x=450, y=250, height=40, width=400)
            # inputField.focus()
            # inputField.bind('<Return>', self.startScan)