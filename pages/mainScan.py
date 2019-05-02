# Import tkinter packages
import Tkinter as tk
from PIL import Image, ImageTk
from ui import create_rounded_rectangle, colors


# Import system Packages
import Queue as queue
import time
import sys
sys.path.append("..")

# Import server
from utils.scanner import Quantifier

# import Scanner
import xml.etree.ElementTree as ET
from functools import partial
from threading import Semaphore, Thread
from openvas_lib import VulnscanManager, VulnscanException

import pages

class MainScan(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg=colors.DWHITE)
        self.root = root

        t = Thread(target = self._loadView)
        t.start()

        t2 = Thread(target = self._startScan)
        t2.start()

    def status(self, i):
        print(str(int(i)) + "%")
        toPrint = "Scanning " + str(int(i)) + "%"
        self.itemconfig(self.loader, text=toPrint, fill=colors.DGRAY)
    
    def toggleNext(self, event=None):
        self.root.changeScreen(pages.Details)

    def scan(self, input_targets):
        # Merge targets into one string separated by comma
        targets = ""
        for i in range(0, len(input_targets)-1):
            targets += input_targets[i] + ", "
        targets += input_targets[len(input_targets)-1]
        print("SCANNING TARGET NETWORK: %s" % targets)

        sem = Semaphore(0)
        manager = VulnscanManager("localhost", "david", "password")

        scan_id, target_id = manager.launch_scan(targets,
                            profile = "Full and fast",
                            callback_end = partial(lambda x: x.release(), sem),
                            callback_progress = self.status)
        # Wait
        sem.acquire()

        return(scan_id)

    def _startScan(self):
        input_name = self.root.input_name
        input_importance = map(float, self.root.input_importance)
        input_targets = self.root.input_target

        scan_id = self.scan(input_targets)
       
        quantifier = Quantifier(input_targets, input_importance, input_name, scan_id)
        
        quantifier.quantify_targets()

        for target in input_targets:
            for detail in (quantifier.target_details[target]):
                if 'link' in detail:
                    quantifier._scan_details.addScan({
                        'scan_id': detail['scan_id'],
                        'host': detail['host'],
                        'nvt': detail['nvt'],
                        'score': detail['score'],
                        'summary': detail['summary'],
                        'link': detail['link']
                    })
                else:
                    quantifier._scan_details.addScan({
                        'scan_id': detail['scan_id'],
                        'host': detail['host'],
                        'nvt': detail['nvt'],
                        'score': detail['score'],
                        'summary': detail['summary']
                    })

        ########## RENDER AFTER NETWORK SCAN
        crit = tk.PhotoImage(file='assets/scan/crit_severity.png')
        high = tk.PhotoImage(file='assets/scan/high_severity.png')
        medium = tk.PhotoImage(file='assets/scan/medium_severity.png')
        low = tk.PhotoImage(file='assets/scan/low_severity.png')
        none = tk.PhotoImage(file='assets/scan/none_severity.png')
        next_btn = tk.PhotoImage(file='assets/scan/next.png')
        
        # Insert if statements here
        # IF CRIT
        if quantifier.quantified_score > 8.9:
            self.quantified_state = crit

            self.create_text(500, 180, font=("Lato", 50), text=str(quantifier.quantified_score), fill="red")
            self.create_image(700, 300, image=self.quantified_state, anchor=tk.E)
            self.create_text(500, 420, font=("Lato", 15, "bold"), text='Your network is in critical condition.', fill=colors.DGRAY)
            self.create_text(500, 450, font=("Lato", 15), text='Please follow proper procedures as advised by your network administrator.', fill=colors.DGRAY)
        # IF HIGH
        elif quantifier.quantified_score > 6.9:
            self.quantified_state = high
            
            self.create_text(500, 180, font=("Lato", 50), text=str(quantifier.quantified_score), fill="#F46A00")
            self.create_image(700, 300, image=self.quantified_state, anchor=tk.E)
            self.create_text(500, 420, font=("Lato", 15, "bold"), text='Your network is highly vulnerable.', fill=colors.DGRAY)
            self.create_text(500, 450, font=("Lato", 15), text='Please follow proper procedures as advised by your network administrator.', fill=colors.DGRAY)
        # IF medium
        elif quantifier.quantified_score > 3.9:
            self.quantified_state = medium
            
            self.create_text(500, 180, font=("Lato", 50), text=str(quantifier.quantified_score), fill="#8E00AA")
            self.create_image(700, 300, image=self.quantified_state, anchor=tk.E)
            self.create_text(500, 420, font=("Lato", 15, "bold"), text='Your network is vulnerable.', fill=colors.DGRAY)
            self.create_text(500, 450, font=("Lato", 15), text='Please follow proper procedures as advised by your network administrator.', fill=colors.DGRAY)
        # IF Low
        elif quantifier.quantified_score > 0.0:
            self.quantified_state = low
            
            self.create_text(500, 180, font=("Lato", 50), text=str(quantifier.quantified_score), fill=colors.BLUE)
            self.create_image(700, 300, image=self.quantified_state, anchor=tk.E)
            self.create_text(500, 420, font=("Lato", 15, "bold"), text='Your network has minor vulnerabilities.', fill=colors.DGRAY)
            self.create_text(500, 450, font=("Lato", 15), text='Please follow proper procedures as advised by your network administrator.', fill=colors.DGRAY)
        # IF None
        else:
            self.quantified_state = none
            
            self.create_text(500, 180, font=("Lato", 50), text='0.0', fill="#00FF82")
            self.create_image(700, 300, image=self.quantified_state, anchor=tk.E)
            self.create_text(500, 420, font=("Lato", 15, "bold"), text='Your network is safe.', fill=colors.DGRAY)
            self.create_text(500, 450, font=("Lato", 15), text='No vulnerabilities found.', fill=colors.DGRAY)
        
        # Render button
        self.next_btn = next_btn
        next_btn_hover = tk.PhotoImage(file='assets/scan/next_hover.png')
        self.next_btn_hover = next_btn_hover
        self.create_image(820, 300, image=self.next_btn, tags="NEXT", anchor=tk.E, activeimage=self.next_btn_hover)
        self.tag_bind('NEXT', '<ButtonPress-1>', self.toggleNext)
        ############
    
    def _loadView(self):
        sem = Semaphore()

        sem.acquire()

        # Display Loader 
        self.create_text(500, 80, font=("Lato", 50), text='NETWORK SECURITY SCORE', fill=colors.DGRAY)
        self.loader = self.create_text(515, 560, font=("Lato", 12, "bold"), text='Scanning 0%', fill=colors.DGRAY)
                
        sem.release()
        time.sleep(0.25)