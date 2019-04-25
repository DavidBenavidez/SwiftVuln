# Import tkinter packages
import Tkinter as tk
from PIL import Image, ImageTk
from utils import colors
from ui import create_rounded_rectangle

# Import matplotlib packages
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")

# Import system Packages
import operator
import menu
import sys
sys.path.append("..")

from server import scanDetailsFuncs, scanFuncs
from datetime import date

class Main(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg=colors.DWHITE)
        
        self.root = root
        self._loadView()
     

    def toggleScan(self, event=None):
        self.root.changeScreen(menu.Scan)
        
    def toggleDetails(self, event=None):
        self.root.changeScreen(menu.Details)    
    
    def getHostsData(self, setVar):
            labels = []
            sizes = []
            host_data = []

            date_range = ["This Month", "Last 3 Months", "Last 6 Months", "Last Year"]
            db = scanDetailsFuncs()
            db2 = scanFuncs()

            # By month
            if setVar.get() == date_range[0]: 
                scans_list = db2.getScansByRange(str(date.today()),1)
            # Last 3 montjs
            elif setVar.get() == date_range[1]:
                scans_list = db2.getScansByRange(str(date.today()),3)
            # Last 6 months
            elif setVar.get() == date_range[2]:
                scans_list = db2.getScansByRange(str(date.today()),6)
            # Last 12 months
            elif setVar.get() == date_range[3]:
                scans_list = db2.getScansByRange(str(date.today()),12)
            
            if (not scans_list):
                return [], []
            
            for scanid in scans_list:
                vuln_data = db.getScanDetails(scanid)
                # Put each host in an arry
                for data in vuln_data:
                    if data.host not in labels:
                        labels.append(data.host)
            
            # Get host count
            for host in labels:
                host_data.append(( str(host), db.getHostCount(host) ))

            # Get only the top 4 hosts
            host_data.sort(key = operator.itemgetter(1), reverse=True)
            host_data = host_data[:4]

            labels = []
            for data in host_data:
                labels.append(data[0])
                sizes.append(data[1])

            return labels, sizes

    def getNVTsData(self, setVar):
            labels = ['medium (4.0-6.9)', 'high (7.0-10.0)']
            date_range = ["This Month", "Last 3 Months", "Last 6 Months", "Last Year"]
            sizes = [0, 0]
            
            scans_list = []
            nvt_data = []
            db = scanDetailsFuncs()
            db2 = scanFuncs()

            # By month
            if setVar.get() == date_range[0]: 
                scans_list = db2.getScansByRange(str(date.today()),1)
            # Last 3 montjs
            elif setVar.get() == date_range[1]:
                scans_list = db2.getScansByRange(str(date.today()),3)
            # Last 6 months
            elif setVar.get() == date_range[2]:
                scans_list = db2.getScansByRange(str(date.today()),6)
            # Last 12 months
            elif setVar.get() == date_range[3]:
                scans_list = db2.getScansByRange(str(date.today()),12)

            
            if (not scans_list):
                return [], []
            # Get cvss scores
            for scanid in scans_list:
                # Get scans by ID
                vuln_data = db.getScanDetails(scanid)
                for data in vuln_data:
                    if data.cvss_score < 7:
                        sizes[0] += 1
                    else:
                        sizes[1] += 1

            return labels, sizes

    def _loadView(self):
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
            

            self.create_image(145, 120, image=self.dash, anchor=tk.W)
            self.create_text(172, 170, text='DASHBOARD', fill=colors.DGRAY)
            
            self.create_image(145, 300, image=self.scan_off, anchor=tk.W, tags="SCAN_SWITCH", activeimage=self.scan)
            self.create_text(172, 350, text='SCAN', fill=colors.GRAY)
            
            self.create_image(145, 480, image=self.details_off, anchor=tk.W, tags="DETAILS_SWITCH", activeimage=self.details)
            self.create_text(172, 530, text='DETAILS', fill=colors.GRAY)

            self.tag_bind('SCAN_SWITCH','<ButtonPress-1>', self.toggleScan)
            self.tag_bind('DETAILS_SWITCH','<ButtonPress-1>', self.toggleDetails)

            # input Range MatPlot
            setVar = tk.StringVar(self)
            setVar.set("This Month")
            optionList = ["This Month", "Last 3 Months", "Last 6 Months", "Last Year"]
            dropMenu = tk.OptionMenu(self, setVar, *optionList)
            dropMenu.place(x=350,y=50)
            
            # MATPLOT ===============================
            # Get Host data
            labels, sizes = self.getHostsData(setVar)
            # Print no data if no data was found
            if(len(labels) == 0):
                self.create_text(800, 165, font=("Helvetica", 15), text='NO DATA', fill='red')
            else:
                # Plot Top hosts
                colors_pie = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
                explode = [0.1, 0, 0, 0]
                colos_pie= colors_pie[:len(labels)]
                explode= explode[:len(labels)]
                f2 = Figure(figsize=(3, 3), dpi=100, facecolor=colors.DWHITE)
                fsub2 = f2.add_subplot(111)
                fsub2.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', shadow=True, startangle=140)
                fsub2.axis('equal')

                canvas = FigureCanvasTkAgg(f2, self)
                def animate2(i):
                    labels, sizes = self.getHostsData(setVar)
                    fsub2.clear()
                    fsub2.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', shadow=True, startangle=140)
                ani2 = animation.FuncAnimation(f2, animate2)

                canvas.draw()
                canvas.get_tk_widget().pack(anchor='e', ipadx=50)
                
            # Get nvt data
            labels, sizes = self.getNVTsData(setVar)
            # Print no data if no data was found
            if(len(labels) == 0):
                self.create_text(800, 480, font=("Lato", 15, "bold"), text='NO DATA', fill='red')
            else:
                # Plot top nvts
                colors_pie = ['gold', 'yellowgreen']
                explode = [0.1, 0]
                colors_pie = colors_pie[:len(labels)]
                explode = explode[:len(labels)]
                f = Figure(figsize=(3, 3), dpi=100, facecolor=colors.DWHITE)
                fsub = f.add_subplot(111)
                fsub.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', shadow=True, startangle=140)
                plt.axes([10,10,10,10])
                fsub.axis('equal')

                canvas = FigureCanvasTkAgg(f, self)
                # Animate Graph // Update everytime
                def animate(i):
                    labels, sizes = self.getNVTsData(setVar)
                    fsub.clear()
                    fsub.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', shadow=True, startangle=140)
            
                ani = animation.FuncAnimation(f, animate) 
                
                canvas.draw()
                canvas.get_tk_widget().pack(anchor='e', ipadx=50)
            # MATPLOT ===============================
            self.create_text(520, 165, font=("Lato", 15, "bold"), text='TOP HOSTS', fill=colors.DGRAY)
            self.create_text(525, 480, font=("Lato", 15, "bold"), text='TOP NVTS', fill=colors.DGRAY)