# Import tkinter packages
import tkinter as tk
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
            scans_listbox = tk.Listbox(self, height=22, width=60, font=('Lato', 12), fg=colors.DGRAY, cursor="mouse")
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
                scan_id = str(value).split(" ")[2]
                scan_id = scan_id.strip("()")

                value = str(value).split(" ")
                # Get data
                details_db = scanDetailsFuncs()
                scan_details = details_db.getScanDetails(scan_id)

                # Instantiate new window
                # self.config(state="disabled")
                top=tk.Toplevel()
                top.title(value[1])
                top.geometry('600x600')
                title = ("TOP NVTS FOR %s" % value[1])
                canvas = tk.Canvas(top, bg=colors.DWHITE, width = 600, height = 600)
                canvas.create_text(150, 30, font=("Lato", 15, 'bold'), text=title, fill=colors.DGRAY)

                listbox = tk.Listbox(top, height=30, width=74, font=('Lato', 10), fg=colors.DGRAY)
                scroll = tk.Scrollbar(top, command=listbox.xview)
                counter = 1
                if len(scan_details):
                    for detail in scan_details:
                        listbox.insert(counter, "NVT: ")
                        counter += 1
                        listbox.insert(counter, "%s" % (detail.nvt))
                        counter += 1
                        listbox.insert(counter, "HOST: ")
                        counter += 1
                        listbox.insert(counter, "%s" % (detail.host))
                        counter += 1
                        listbox.insert(counter, "CVSS SCORE: ")
                        counter += 1
                        listbox.insert(counter, "%s" % (detail.cvss_score))
                        counter += 1
                        listbox.insert(counter, "SUMMARY: ")
                        counter += 1
                        listbox.insert(counter, "%s" % (detail.summary))
                        counter += 1
                        # listbox.insert(counter, "\n\n")
                        # counter += 1
                else:
                    listbox.insert(counter, "No major Vulnerabilities Found")

                
                listbox.place(x=2, y=50)
                                
                canvas.pack()

                top.resizable(0,0)
                top.mainloop()
                



            self.create_text(637, 65, font=("Lato", 15, "bold"), text='LIST OF SCANS', fill=colors.DGRAY)
            self.create_text(635, 85, font=("Lato", 9), text='0) Scan_Name (Scan ID)', fill=colors.DGRAY)
            # self.create_text(0, 0, font=("Lato", 15, "bold"), text='TOP NVTS', fill=colors.DGRAY)
            # Initialize Listbox
            scans_listbox.bind('<<ListboxSelect>>', onselect)
            scans_listbox.place(x=370, y=100)

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