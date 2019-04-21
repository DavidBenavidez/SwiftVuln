import tkinter as tk
from utils.fonts import _getFont

class Button(tk.Canvas):
  def __init__(self, root, text, bg='magenta', command=None):
    self._canvas = tk.Canvas.__init__(self, root, width=430, height=75, bd=0, highlightthickness=0, bg=bg)
    
    normal = tk.PhotoImage(file='assets/ui/button.png')
    toggled = tk.PhotoImage(file='assets/ui/button-toggle.png')

    self.normal = normal
    self.toggled = toggled
    self.text = text
    self._command = command

    self.create_image(-1, -1, image=self.normal, anchor=tk.NW)
    self.create_text(430/2, 75/2, font=_getFont('title2'), text=self.text)

    self.bind('<Button-1>', self._clickOn)
    self.bind('<ButtonRelease-1>', self._clickOff)

  def _clickOn(self, event=None):
    self.create_image(-1, -1, image=self.toggled, anchor=tk.NW)
    self.create_text(430/2, 75/2, font=_getFont('title2'), text=self.text)

  def _clickOff(self, event=None):
    self.create_image(-1, -1, image=self.normal, anchor=tk.NW)
    self.create_text(430/2, 75/2, font=_getFont('title2'), text=self.text)

    if self._command:
      self._command()
