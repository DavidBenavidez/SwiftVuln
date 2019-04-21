import Tkinter as tk 
from os import _exit

import menu


class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('SwiftVuln')
        self._screen = None
        self.changeScreen(menu.Main)
    
    def handleWindowClose(self):
        self.destroy()
        _exit(0)
    
    def changeScreen(self, screen):
        next = screen(self)

        if self._screen is not None:
            self._screen.destroy()

        self._screen = next
        self._screen.pack(expand=1, fill=tk.BOTH)

if __name__ == '__main__':
    app = MainApplication()

    width, height = app.winfo_screenwidth(), app.winfo_screenheight()

    app.geometry('%dx%d+0+0' % (width,height))
    app.resizable(0, 0)
    
    app.mainloop()