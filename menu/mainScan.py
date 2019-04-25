# Import tkinter packages
import tkinter as tk
from PIL import Image, ImageTk
from utils import colors
from ui import create_rounded_rectangle


# Import system Packages
import menu
import sys
sys.path.append("..")

class MainScan(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg=colors.DWHITE)
        self.root = root
        self._loadView()
    
    def toggleBack(self, event=None):
        self.root.changeScreen(menu.StartScan)
    
    def _loadView(self):
            back = tk.PhotoImage(file='assets/buttons/back.png')
            back_hover = tk.PhotoImage(file='assets/buttons/back_hover.png')
            self.back = back
            self.back_hover = back_hover
            self.create_image(180, 100, image=self.back, anchor=tk.E, tags="BACK", activeimage=self.back_hover)
            self.tag_bind('BACK', '<ButtonPress-1>', self.toggleBack)
    
            if self.root.scan_type == "One":
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
                    text='Enter Comma-Seprated Hosts:',
                    fg='Black',
                    bg=colors.DWHITE,
                    font='Lato'
                )
                importanceField = tk.Entry(
                    self,
                    textvariable="lala2",
                    bg=colors.DGRAY,
                    fg=colors.WHITE,
                    highlightcolor=colors.GRAY,
                    justify=tk.CENTER,
                    font='Lato'
                )
                importanceLabel = tk.Label(
                    self,
                    text='Enter Comma-Seprated Importance:',
                    fg='Black',
                    bg=colors.DWHITE,
                    font='Lato'
                )
                fieldLabel.place(x=530, y=230, anchor='center')
                inputField.place(x=330, y=250, height=40, width=400)
                inputField.focus()

                importanceLabel.place(x=530, y=330, anchor='center')
                importanceField.place(x=330, y=350, height=40, width=400)
                importanceField.focus()
            else:
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
                    text='Enter Subnet:',
                    fg='Black',
                    bg=colors.DWHITE,
                    font='Lato'
                )
                fieldLabel.place(x=530, y=230, anchor='center')
                inputField.place(x=330, y=250, height=40, width=400)
                inputField.focus()