import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Main GUI properties 
APP_WIDTH  = 500
APP_HEIGHT = 500
APP_BORDER = 10

# Brief class to manage the application GUI & ACTIONS
class MainWindow(ttk.Frame):
    def __init__(self, master) -> None:
        self.InitializeInterface(master)
    
    # Brief function for initializing interface
    def InitializeInterface(self, master) -> None:
        super().__init__(master)
        self.grid(column=0, row=0, sticky="nsew")

        # Creation of the main window container
        windowContainer = ttk.Frame(self)
        windowContainer.grid(column=0, row=0, sticky="nsew")

        # Creation of the container for every widgets
        widgetsContainer = ttk.Frame(windowContainer)
        widgetsContainer.grid(column=0, row=0, sticky="nsew")

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
    WindowGeometry(app, APP_WIDTH, APP_HEIGHT)
    MainWindow(app)
    app.mainloop()

if __name__ == "__main__":
    Main()