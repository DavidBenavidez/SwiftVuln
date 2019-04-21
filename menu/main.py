import Tkinter as tk 
import menu

class Main(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=700, height=600, bd=0, highlightthickness=0, bg='blue')
        self.root = root

        # self._loadView()

        # def _loadView(self):
            
