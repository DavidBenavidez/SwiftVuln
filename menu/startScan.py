# Import tkinter packages
import Tkinter as tk
from PIL import Image, ImageTk
from utils import colors
from ui import create_rounded_rectangle


# Import system Packages
import menu
import sys
sys.path.append("..")

class StartScan(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg=colors.DWHITE)
        self.root = root   
        self._loadView()
    
    def toggleMain(self, event=None):
        self.root.changeScreen(menu.Main)
         
    def toggleDetails(self, event=None):
        self.root.changeScreen(menu.Details)
        
    def _loadView(self):
            # SIDE NAVBAR
           #########################################################  
            # self.create_text(520, 165, font=("Lato", 15, "bold" ), text='TOP HOSTS', fill=colors.DGRAY)

            inputField = tk.Entry(
                self,
                textvariable="lala",
                bg=colors.DGRAY,
                fg=colors.WHITE,
                highlightcolor=colors.GRAY,
                justify=tk.CENTER,
                font='Lato'
            )
            fieldLabel = tk.Label(
                self,
                text='Enter target',
                fg='Black',
                bg=colors.DWHITE,
                font='Lato'
            )
            fieldLabel.place(x=650, y=230, anchor='center')
            inputField.place(x=450, y=250, height=40, width=400)
            inputField.focus()