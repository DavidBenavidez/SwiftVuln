# Import tkinter packages
import Tkinter as tk
from PIL import Image, ImageTk
from utils import colors

# Import system Packages
from threading import Semaphore, Thread
import subprocess
import time
import sys
sys.path.append("..")

import pages

from whichcraft import which

class CheckSetup(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg=colors.DWHITE)
        self.root = root
        
        self._loadView()

    def _checkOpenvas(self, name):
        """Check whether `name` is on PATH and marked as executable."""
        return which(name) is not None

    def _updateOpenVAS(self):
        self.yes.destroy()
        self.no.destroy()
        self.itemconfig(self.loader, text='Updating OpenVAS\' Feeds... (Can take up to 20 Minutes)', fill=colors.DGRAY)
        def update():
            try:
                result = str(subprocess.check_output(['bash', '-c', './update-openvas'])) # Update openVAS
                # initialize openvas
                t2 = Thread(target = self._initOpenVAS)
                t2.start() 
            except Exception as e:
                self.itemconfig(self.loader, text='Error updating OpenVAS feeds. Error: %s' % e, fill="red")
                def exitApp():
                    self.root.destroy()
                self.exit = tk.Button(self, bg=colors.DGRAY, fg=colors.WHITE, text="exit", command=exitApp)
                self.exit.place(x=490, y=555)
                           
        
        t = Thread(target = update)
        t.start()

    def _initOpenVAS(self):
        self.yes.destroy()
        self.no.destroy()
        self.itemconfig(self.loader, text='Initializing OpenVAS...', fill=colors.DGRAY)
        def update():
            subprocess.check_output(['bash', '-c', './start-openvas']) # Initialize openVAS
            self.root.changeScreen(pages.Scan)
           
        t = Thread(target = update)
        t.start()
 

    def _loadView(self):
        if(self._checkOpenvas("openvas-start")):
            self.create_text(515, 500, font=("Lato", 12, "bold"), text='OpenVAS installed.', fill="green")
            self.loader = self.create_text(515, 530, font=("Lato", 12, "bold"), text='Would you like to update OpenVAS\' feeds?', fill=colors.DGRAY)
            self.yes = tk.Button(self, text="Yes", bg=colors.DGRAY, fg=colors.WHITE,command=self._updateOpenVAS)
            self.yes.place(x=440, y=555)
            self.no = tk.Button(self, text="No", bg=colors.DGRAY, fg=colors.WHITE, command=self._initOpenVAS)
            self.no.place(x=530, y=555)
        else:
            self.loader = self.create_text(515, 560, font=("Lato", 12, "bold"), text='OpenVAS not detected. Please install OpenVAS.', fill="red")

    