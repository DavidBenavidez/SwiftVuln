# Import tkinter packages
import Tkinter as tk
from PIL import Image, ImageTk
from utils import colors
from ui import create_rounded_rectangle


# Import system Packages
import menu
import sys
sys.path.append("..")

# Import server
from server import scanFuncs, scanDetailsFuncs

class Details(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg=colors.DWHITE)

        self.root = root   
        self._loadView()
    
    def toggleMain(self, event=None):
        self.root.changeScreen(menu.Main)
     
    def toggleScan(self, event=None):
        self.root.changeScreen(menu.Scan)
        
        
    def _loadView(self):
            # Get data
            scan_list_db = scanFuncs()
            scan_list = scan_list_db.getScans()

            # Initialize Listbox
            scans_listbox = tk.Listbox(self, height=22, width=60, font=('Helvetica', 12, 'bold'), fg=colors.DGRAY, cursor="mouse")
            scroll = tk.Scrollbar(self, command=scans_listbox.yview)

            counter = 1
            for scan in scan_list:
                scans_listbox.insert(counter, "%d) %s (%s)" % (counter, scan.scan_name, scan.scan_id))
                counter += 1

            # Initialize listbox listener
            def onselect(evt):
                # Note here that Tkinter passes an event object to onselect()
                w = evt.widget
                index = int(w.curselection()[0])
                value = w.get(index)
                print('You selected item %d: "%s"' % (index, value))
                # Get scan id
                value = str(value).split(" ")[2]
                scan_id = value.strip("()")
                print(scan_id)

            scans_listbox.bind('<<ListboxSelect>>', onselect)
            scans_listbox.place(x=370, y=37)

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
            
            self.create_image(145, 300, image=self.scan_off, anchor=tk.W, tags="SCAN_SWITCH", activeimage=self.scan)
            self.create_text(172, 350, text='SCAN', fill=colors.GRAY)
            
            self.create_image(145, 480, image=self.details, anchor=tk.W)
            self.create_text(172, 530, text='DETAILS', fill=colors.DGRAY)

            self.tag_bind('MAIN_SWITCH','<ButtonPress-1>', self.toggleMain)
            self.tag_bind('SCAN_SWITCH','<ButtonPress-1>', self.toggleScan)