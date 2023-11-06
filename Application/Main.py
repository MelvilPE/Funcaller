import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os

import View.InterfaceView as InterfaceView

# Gloal consts variables that are specified here can be accessed from others script
APP_WIDTH  = 648
APP_HEIGHT = 550

SCRIPT_NAME = os.path.basename(__file__)
SCRIPT_ROOT = os.path.dirname(__file__)
SCRIPT_PATH = __file__

INTERNAL_PROJECT_NAME = "ApplicationInternal"

# Brief function to resize and centering the interface
def WindowGeometry(window, width, height) -> None:
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry("{}x{}+{}+{}".format(width, height, x, y - 20))

# Main function at application startup
def Main() -> None:
    app = ttk.Window(
        title="Funcaller", 
        themename="superhero", 
        resizable=(False, False)
    )
    app.iconbitmap("icon.ico")
    WindowGeometry(app, APP_WIDTH, APP_HEIGHT)
    InterfaceView.MainWindow(app)
    app.mainloop()

if __name__ == "__main__":
    Main()