from tkinter import font

def _getFont(fontClass):
  fonts = {
    'hero': font.Font(family='8BIT WONDER', size=72),
    'title': font.Font(family='Press Start 2P', size=24),
    'title2': font.Font(family='Press Start 2P', size=16),
    'title3': font.Font(family='Press Start 2P', size=12),
    'body': font.Font(family='Silom', size=12),
    'body2': font.Font(family='Silom', size=14),
    'body3': font.Font(family='Silom', size=16),
    'body4': font.Font(family='Silom', size=22),
    'heading-2s': font.Font(family='Gulkave', size=14),
    'heading': font.Font(family='Gulkave', size=22),
    'heading-2x': font.Font(family='Gulkave', size=26),
    'heading-3x': font.Font(family='Gulkave', size=32),
  }

  return fonts[fontClass]
