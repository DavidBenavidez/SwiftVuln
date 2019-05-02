# Import tkinter packages
import Tkinter as tk
from PIL import Image, ImageTk
from ui import create_rounded_rectangle, colors


# Import subnet calculator
import ipcalc

# Import system Packages
import sys
import time
sys.path.append("..")

import pages

class ConfigScan(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg=colors.DWHITE)
        self.root = root
        self.input_name = tk.StringVar()
        self.input_target = tk.StringVar()
        self.input_importance = tk.StringVar()
        self.input_target_subnet = tk.Variable()
        self.input_importance_subnet = tk.Variable()
        self.input_subnet = tk.StringVar()

        self.importance_range = [0.4, 0.6, 0.8, 1.6, 2.0]
        self._loadView()
    
    def toggleBack(self, event=None):
        self.root.changeScreen(pages.InitScan)
    
    def checkInputsOne(self, event=None):
        # Check value of inputs if one by one input of hosts was chosen
        input_name = str(self.input_name.get())
        input_target = str(self.input_target.get()).replace(" ", "") # Remove whitespace
        input_importance = str(self.input_importance.get()).replace(" ", "") # Remove Whitespace
        
        input_target = input_target.split(",")
        input_importance = input_importance.split(",")
        
        input_target = filter(None, input_target)
        input_importance = filter(None, input_importance)
        flag = 0

        if not input_target or not input_importance or not input_name:
            self.itemconfig(self.err, text='Fill out all the the fields', fill="red")
        elif ( (len(input_target) != len(input_importance)) or not (input_target) or not(input_importance) ):
            self.itemconfig(self.err, text='Number of hosts and importance are not the same.', fill="red")
        else:
            for importance_value in input_importance:
                if(float(importance_value) not in self.importance_range):
                    flag = 1
                    self.itemconfig(self.err, text='Invalid Importance Value', fill="red")
            if flag == 0:
                self.root.input_name = input_name
                self.root.input_target = input_target
                self.root.input_importance = input_importance
                self.root.changeScreen(pages.MainScan)
            flag = 0
    def checkInputsSubnet(self, event=None):
        # Check value of inputs if one by one input of hosts was chosen
        # if 
        def removeIndex(value):
            # Remove spaces
            value = value.replace(" ", "")
            value = value.split(")")[1]
            return(value)

        flag = 0
        if not self.input_name.get() or not self.input_subnet.get() or not self.input_importance_subnet.get():
            self.itemconfig(self.err, text='Fill out all the the fields', fill="red")
        else:
            self.input_importance = map(float, map(removeIndex, self.input_importance_subnet.get()))
            self.input_target = map(str, map(removeIndex, self.input_target_subnet.get()))
            for importance_value in self.input_importance:
                if(importance_value not in self.importance_range):
                    flag = 1
                    self.itemconfig(self.err, text='Invalid Importance Value', fill="red")

            if flag == 0:
                self.root.input_name = self.input_name.get()
                self.root.input_target = self.input_target
                self.root.input_importance = self.input_importance
                self.root.changeScreen(pages.MainScan)
            flag = 0

    def _getSubnets(self, event=None):
        try:
            network = ipcalc.Network(self.input_subnet.get())
            self.listbox_hosts.delete('0', 'end')
            self.listbox_imp.delete('0', 'end')
            counter = 1
            for host in network:
                self.listbox_hosts.insert(counter, str(counter) + ') ' + str(host))
                self.listbox_imp.insert(counter, str(counter) + ') ' + '0.4')
                counter += 1

            self.itemconfig(self.err, text='', fill=colors.DWHITE)
        except ValueError:
            self.itemconfig(self.err, text='Please Enter a valid Subnet', fill="red")

    def _changeImp(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        try:
            index = int(w.curselection()[0])
            value = w.get(index)
            newImpValue = tk.StringVar()

            def setImportance(evt, event=None):
                self.listbox_imp.delete(index)
                self.listbox_imp.insert(index, str(index+1) + ') ' + str(newImpValue.get()))

            # get new importance
            newImp = tk.Entry(
                self,
                textvariable=newImpValue,
                bg=colors.DGRAY,
                fg=colors.WHITE,
                highlightcolor=colors.GRAY,
                justify=tk.CENTER,
                font='Lato'
            )
            impLabel = tk.Label(
                self,
                text='Change Importance:',
                fg='Black',
                bg=colors.DWHITE,
                font='Lato'
            )
            impExampleLabel = tk.Label(
                self,
                text='Enter value from 0.4, 0.8, 1.2, 1.6, and 2.0',
                fg='Black',
                bg=colors.DWHITE,
                font=('Lato', 9)
            )

            impLabel.place(x=130, y=380, anchor='center')
            newImp.place(x=80, y=400, height=30, width=100)
            impExampleLabel.place(x=130, y=450, anchor='center')
            impLabel.focus()
            newImp.bind('<Return>', setImportance)
        except:
            print("None Selected")


    def _loadView(self):
        logo = tk.PhotoImage(file='assets/buttons/logo_blue.png')
        back = tk.PhotoImage(file='assets/buttons/back.png')
        back_hover = tk.PhotoImage(file='assets/buttons/back_hover.png')
        submit_img = tk.PhotoImage(file='assets/scan/submit.png')
        check_subnet_img = tk.PhotoImage(file='assets/scan/check_subnet.png')

        self.logo = logo
        self.back = back
        self.submit_img = submit_img
        self.back_hover = back_hover
        self.submit_img = submit_img
        self.check_subnet_img = check_subnet_img

        self.create_image(900, 100, image=self.logo, anchor=tk.E)
        self.create_image(180, 100, image=self.back, anchor=tk.E, tags="BACK", activeimage=self.back_hover)

        self.tag_bind('BACK', '<ButtonPress-1>', self.toggleBack)

        # Render input fields for one by one input
        if self.root.scan_type == "One":
            nameField = tk.Entry(
                self,
                textvariable=self.input_name,
                bg=colors.DGRAY,
                fg=colors.WHITE,
                highlightcolor=colors.GRAY,
                justify=tk.CENTER,
                font='Lato'
            )
            nameLabel = tk.Label(
                self,
                text='Enter Scan Name:',
                fg='Black',
                bg=colors.DWHITE,
                font='Lato'
            )
            inputField = tk.Entry(
                self,
                textvariable=self.input_target,
                bg=colors.DGRAY,
                fg=colors.WHITE,
                highlightcolor=colors.GRAY,
                justify=tk.CENTER,
                font='Lato'
            )
            fieldLabel = tk.Label(
                self,
                text='Enter Comma-Separated Hosts:',
                fg='Black',
                bg=colors.DWHITE,
                font='Lato'
            )
            hostExampleLabel = tk.Label(
                self,
                text='e.g (10.0.5.28, 10.0.5.4, 10.0.4.141)',
                fg='Black',
                bg=colors.DWHITE,
                font=('Lato', 9)
            )
            importanceField = tk.Entry(
                self,
                textvariable=self.input_importance,
                bg=colors.DGRAY,
                fg=colors.WHITE,
                highlightcolor=colors.GRAY,
                justify=tk.CENTER,
                font='Lato'
            )
            importanceLabel = tk.Label(
                self,
                text='Enter Comma-Separated Importance:',
                fg='Black',
                bg=colors.DWHITE,
                font='Lato'
            )
            exampleLabel = tk.Label(
                self,
                text='Must be in range (0.4, 0.8, 1.2, 1.6, 2.0)',
                fg='Black',
                bg=colors.DWHITE,
                font=('Lato', 9)
            )
            exampleLabel2 = tk.Label(
                self,
                text='e.g: (0.4, 0.4, 1.0)',
                fg='Black',
                bg=colors.DWHITE,
                font=('Lato', 9)
            )
        
            nameLabel.place(x=530, y=170, anchor='center')
            nameField.place(x=330, y=190, height=40, width=400)
            
            fieldLabel.place(x=530, y=260, anchor='center')
            inputField.place(x=330, y=280, height=40, width=400)
            hostExampleLabel.place(x=330, y=320, height=40, width=400)

            importanceLabel.place(x=530, y=380, anchor='center')
            importanceField.place(x=330, y=400, height=40, width=400)
            exampleLabel.place(x=330, y=435, height=40, width=400)
            exampleLabel2.place(x=330, y=465, width=400)
            
            submit = tk.Button(self, text="Start Scan", command=self.checkInputsOne)
            submit.config(image=self.submit_img)
            submit.place(x=443, y=510)

            self.err = self.create_text(538, 570, font=("Lato", 12, "bold"), text='Number of hosts and importance are not the same.', fill=colors.DWHITE)
        else:
            nameField = tk.Entry(
                self,
                textvariable=self.input_name,
                bg=colors.DGRAY,
                fg=colors.WHITE,
                highlightcolor=colors.GRAY,
                justify=tk.CENTER,
                font='Lato'
            )
            nameLabel = tk.Label(
                self,
                text='Enter Scan Name:',
                fg='Black',
                bg=colors.DWHITE,
                font='Lato'
            )
            inputField = tk.Entry(
                self,
                textvariable=self.input_subnet,
                bg=colors.DGRAY,
                fg=colors.WHITE,
                highlightcolor=colors.GRAY,
                justify=tk.CENTER,
                font='Lato'
            )
            fieldLabel = tk.Label(
                self,
                text='Enter Subnet: ',
                fg='Black',
                bg=colors.DWHITE,
                font='Lato'
            )

            # instantiate list box
            # Instantiate list box label
            self.create_text(390, 330, font=("Lato", 10, "bold"), text="HOSTS", fill=colors.DGRAY)
            self.create_text(305, 330, font=("Lato", 10, "bold"), text="IMPORTANCE", fill=colors.DGRAY)
            
            self.listbox_imp = tk.Listbox(self, listvariable = self.input_importance_subnet, height=7, width=54, font=('Lato', 10), fg=colors.DGRAY)
            scroll_imp = tk.Scrollbar(self, command=self.listbox_imp.xview)

            self.listbox_hosts = tk.Listbox(self, listvariable=self.input_target_subnet, height=7, width=54, font=('Lato', 10), fg=colors.DGRAY)
            scroll_hosts = tk.Scrollbar(self, command=self.listbox_hosts.xview)
            
            # Place inputs
            nameLabel.place(x=530, y=130, anchor='center')
            nameField.place(x=330, y=150, height=40, width=400)
            nameLabel.focus()

            fieldLabel.place(x=530, y=230, anchor='center')
            inputField.place(x=330, y=250, height=40, width=400)
            inputField.focus()

            # Button to check subnet
            check_subnet = tk.Button(self, text="Input Subnet", command=self._getSubnets)
            check_subnet.config(image=self.check_subnet_img)
            check_subnet.place(x=760, y=255)

            self.listbox_hosts.place(x = 360, y = 350)
            # Add lister for importance
            self.listbox_imp.bind('<<ListboxSelect>>', self._changeImp)
            self.listbox_imp.place(x = 260, y = 350)
            self.listbox_imp.focus()

            # Edit this to go to mainScan and pass the proper variables
            submit = tk.Button(self, text="Start Scan", command=self.checkInputsSubnet)
            submit.config(image=self.submit_img)
            submit.place(x=450, y=500)

            self.err = self.create_text(543, 560, font=("Lato", 12, "bold"), text='Number of hosts and importance are not the same.', fill=colors.DWHITE)