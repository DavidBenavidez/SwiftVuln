# Import tkinter packages
import Tkinter as tk
from PIL import Image, ImageTk
from utils import colors
from ui import create_rounded_rectangle


# Import system Packages
import pages
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
        self.root.changeScreen(pages.Main)
     
    def toggleScan(self, event=None):
        self.root.changeScreen(pages.Scan)
        
        
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
        
        self.create_image(145, 310, image=self.scan_off, anchor=tk.W, tags="SCAN_SWITCH", activeimage=self.scan)
        self.create_text(172, 350, text='SCAN', fill=colors.GRAY)
        
        self.create_image(145, 470, image=self.details, anchor=tk.W)
        self.create_text(172, 520, text='DETAILS', fill=colors.DGRAY)

        self.tag_bind('MAIN_SWITCH','<ButtonPress-1>', self.toggleMain)
        self.tag_bind('SCAN_SWITCH','<ButtonPress-1>', self.toggleScan)
        # Get data
        self.scans_db = scanFuncs()
        scan_list = self.scans_db.getScans()
        scans_listbox = tk.Listbox(self, height=22, width=60, font=('Lato', 12), fg=colors.DGRAY, cursor="mouse")
        scroll = tk.Scrollbar(self, command=scans_listbox.yview)

        counter = 1
        for scan in scan_list:
            scans_listbox.insert(counter, "%d) %s (%s)" % (counter, scan.scan_name, scan.scan_id))
            counter += 1

        # Initialize listbox listener
        def onselect(evt):
            def deleteScan():
                # Delete Scan
                self.scans_db.deleteScan(self.scan_id)
                self.details_db.deleteScan(self.scan_id)
                top.destroy()
                self.root.changeScreen(pages.Details)

            # Note here that Tkinter passes an event object to onselect()
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            # Get scan id
            scan_id = str(value).split(" ")
            scan_id = str(scan_id[len(scan_id)-1])
            scan_id = scan_id.strip("()")
            
            self.scan_id = scan_id

            value = str(value).split(" ")
            # Get data
            self.details_db = scanDetailsFuncs()
            scan_score = self.scans_db.getScanScore(scan_id)
            scan_date = self.scans_db.getScanDate(scan_id)
            scan_details = self.details_db.getScanDetails(scan_id)

            # Instantiate new window
            # self.config(state="disabled")
            top=tk.Toplevel()
            value = value[1:]
            title = str(' '.join(value[:(len(value)-1)]))
            top.lift()
            top.focus_force()
            top.grab_set()
            top.geometry('600x600')

            canvas = tk.Canvas(top, bg=colors.DWHITE, width = 600, height = 600)
            canvas.create_text(5, 12, anchor="w", font=("Lato", 9), text= (scan_date), fill=colors.DGRAY)
            canvas.create_text(80, 30, font=("Lato", 15, 'bold'), text="TOP NVTS FOR: " , fill=colors.DGRAY)
            canvas.create_text(160, 30, anchor="w", font=("Lato", 15, 'bold'), text=title, fill=colors.VBLUE)
            
            # instantiate list box
            listbox = tk.Listbox(top, height=27, width=74, font=('Lato', 10), fg=colors.DGRAY)
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
                    if(detail.link):
                        listbox.insert(counter, "LINK: ")
                        counter += 1
                        listbox.insert(counter, "%s" % (detail.link))
                        counter += 1
                    listbox.insert(counter, "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    counter += 1
            else:
                listbox.insert(counter, "No major Vulnerabilities Found")

            
            listbox.place(x=2, y=50)
            # Print Quantified Score
            if scan_score > 8.9:
                scan_score = str(scan_score) + " Critical"
                color = "red"
            elif scan_score > 6.9:
                color = "#F46A00"
                scan_score = str(scan_score) + " High"
            elif scan_score > 3.9:
                scan_score = str(scan_score) + " Medium"
                color = "#8E00AA"
            elif scan_score > 0.0:
                scan_score = str(scan_score) + " Low"
                color = colors.BLUE
            else: 
                scan_score = str(scan_score)
                color = "#00FF82"
            canvas.create_text(140, 570, anchor="w", font=("Lato", 15, "bold"), text= scan_score, fill=color)
            canvas.create_text(70, 570, font=("Lato", 15, "bold"), text= "CVSS SCORE: ", fill=colors.DGRAY)
            
             # Delete Button
            delete_btn = tk.Button(top, font=("Lato", 10, "bold"), fg=colors.WHITE, bg="red", text="DELETE SCAN", command=deleteScan, height=1, width=10)
            delete_btn.place(x=475, y=557)

            canvas.pack()

            top.resizable(0,0)
            top.mainloop()
        
        self.create_text(637, 65, font=("Lato", 15, "bold"), text='LIST OF SCANS', fill=colors.VBLUE)
        self.create_text(635, 85, font=("Lato", 9), text='0) Scan_Name (Scan ID)', fill=colors.DGRAY)

        # Initialize Listbox
        scans_listbox.bind('<<ListboxSelect>>', onselect)
        scans_listbox.place(x=370, y=100)