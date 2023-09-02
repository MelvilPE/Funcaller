import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip

import Modules.ProcessUtils as ProcessUtils
import ctypes
import re

# Main GUI properties 
APP_WIDTH  = 648
APP_HEIGHT = 550

# Space properties
BORDER_SPACE = 10
COLUMN_SPACE = 5

# Regex properties
HEX_FORMAT_REGEX = r'^0x[0-9A-Fa-f]+$'

# Brief class to manage the application GUI & ACTIONS
class MainWindow(ttk.Frame):
    def __init__(self, master) -> None:
        self.numberOfParameters = 0
        self.parameterLines = []
        """
        Here we have the graphical attributes (hard-coded)
        Maybe we will move them to a configuration file
        """
        self.eProgramArchitectures = ["x86", "x64"]
        self.eBooleanValues = ["true", "false"]
        self.eParameterTypes = ["String(const char*)", "Bool", "Byte", "Word", "Dword", "Qword"]
        self.eReturnTypes = ["Void"] + self.eParameterTypes
        self.eCallingConventions = ["__cdecl", "__clrcall", "__stdcall", "__fastcall", "__thiscall", "__vectorcall"]
        self.processesList = []
        self.InitializeInterface(master)

    # Brief function for initializing interface
    def InitializeInterface(self, master) -> None:

        def CallFunction() -> None:
            print("Not ready to execute")

        # Prevent the ability to switch tabs on the targeted widget
        def AntiSwitchNotebook(notebook, tabIndex = 0) -> None:
            notebook.select(tabIndex)

        # Brief functions to use the different tabs to add or remove parameters
        def AddOrRemoveParameter(event = None) -> None:
            if event != None:
                AddOrRemoveParameterLegacy(event)
            else:
                AddOrRemoveParameterLegacy(event, True)
        def AddOrRemoveParameterLegacy(event, addFirstParam = False) -> None:
            currTabIndex = 0
            if addFirstParam == True:
                currTabIndex = 1
            else:
                currTabIndex = event.widget.index("current")
            if currTabIndex != 0:
                # The action of the + button
                # We add a new parameter line
                if currTabIndex == 1:
                    if self.numberOfParameters >= 10:
                        ctypes.windll.user32.MessageBoxW(0, "MainGUI::AddOrRemoveParameter Currently impossible to add more than 10 parameters", "Funcaller", 16)
                    else:
                        parameterLine = ttk.Frame(paramsContainerInternal, style="light")
                        if addFirstParam == True:
                            ToolTip(parameterLine, bootstyle=(DANGER, INVERSE), text="Note that the first parameter is empty by default, which means that the function that you are trying to call has no input parameters")

                        cbbParamType = ttk.Combobox(parameterLine, style="light", width=48, values=self.eParameterTypes)
                        cbbParamType.grid(column=0, row=0)
                        
                        cbbParamValue = ttk.Entry(parameterLine, style="light", width=50)
                        cbbParamValue.grid(column=1, row=0)

                        parameterLine.grid(column=0, row=self.numberOfParameters, sticky="nsew")
                        self.parameterLines.append(parameterLine)
                        self.numberOfParameters += 1

                # The action of the - button
                # We remove the last parameter line
                elif currTabIndex == 2 and self.numberOfParameters > 1:
                        self.parameterLines[self.numberOfParameters-1].grid_forget()
                        self.parameterLines.pop()
                        self.numberOfParameters -= 1
            
            # We prevent the tab change since they act like buttons
            AntiSwitchNotebook(paramsContainer)

        def UpdateProcessesList() -> None:
            self.processesList = ProcessUtils.ListRunningProcesses()
            cbbProcessName["values"] = ProcessUtils.ListProcessesNames(self.processesList)
            cbbProcessId["values"] = ProcessUtils.ListProcessesIds(self.processesList)

        def SetProcInfosFromIndex(selectedProcessIndex) -> None:
            cbbProcessName.set(self.processesList[selectedProcessIndex]["name"])
            cbbProcessId.set(self.processesList[selectedProcessIndex]["pid"])

        def OnProcessNameClicked(event) -> None:
            UpdateProcessesList()

        def OnProcessNameSelected(event) -> None:
            selectedIndex = cbbProcessName.current()
            SetProcInfosFromIndex(selectedIndex)

        def OnProcessIdClicked(event) -> None:
            UpdateProcessesList()

        def OnProcessIdSelected(event) -> None:
            selectedIndex = cbbProcessId.current()
            SetProcInfosFromIndex(selectedIndex)

        def OnAdressWritten(event) -> None:
            if cbbArchitecture.get() not in self.eProgramArchitectures:
                cbbFunctionAdress.set("0x")
                ctypes.windll.user32.MessageBoxW(0, "MainGUI::OnAdressWritten Before entering an address, please select an architecture", "Funcaller", 16)
                return
            
            if not re.match(HEX_FORMAT_REGEX, cbbFunctionAdress.get()) and cbbFunctionAdress.get() != "0x":
                cbbFunctionAdress.set("0x")
                ctypes.windll.user32.MessageBoxW(0, "MainGUI::OnAdressWritten Function adress must be in hexadecimal format", "Funcaller", 16)
                return

            if cbbArchitecture.get() == "x86" and len(cbbFunctionAdress.get()) > len("0xFFFFFFFF"):
                cbbFunctionAdress.set("0x")
                ctypes.windll.user32.MessageBoxW(0, "MainGUI::OnAdressWritten For x86 architecture, the address size must be smaller than '0xFFFFFFFF'.", "Funcaller", 16)
                return
            
            if cbbArchitecture.get() == "x64" and len(cbbFunctionAdress.get()) > len("0xFFFFFFFFFFFFFFFF"):
                cbbFunctionAdress.set("0x")
                ctypes.windll.user32.MessageBoxW(0, "MainGUI::OnAdressWritten For x64 architecture, the address size must be smaller than '0xFFFFFFFFFFFFFFFF'.", "Funcaller", 16)
                return

        super().__init__(master)
        self.grid(column=0, row=0, sticky="nsew")

        # Creation of the main window container
        windowContainer = ttk.Frame(self)
        windowContainer.grid(column=0, row=0, sticky="nsew")

        # Creation of the container for every widgets
        widgetsContainer = ttk.Frame(windowContainer)
        widgetsContainer.grid(column=0, row=0, sticky="nsew")

        # Start process properties
        processContainer = ttk.Frame(widgetsContainer)

        lblArchitecture = ttk.Label(processContainer, style="light", text="Program Architecture", justify=CENTER)
        lblArchitecture.grid(column=0, row=0, padx=(BORDER_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")

        cbbArchitecture = ttk.Combobox(processContainer, style="light", values=self.eProgramArchitectures)
        cbbArchitecture.grid(column=0, row=1, padx=(COLUMN_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")

        lblProcessName = ttk.Label(processContainer, style="light", text="Process Name", justify=CENTER)
        lblProcessName.grid(column=1, row=0, padx=(BORDER_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")

        cbbProcessName = ttk.Combobox(processContainer, style="light")
        cbbProcessName.grid(column=1, row=1, padx=(COLUMN_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")
        cbbProcessName.bind('<Button-1>', OnProcessNameClicked)
        cbbProcessName.bind('<<ComboboxSelected>>', OnProcessNameSelected)

        lblProcessId = ttk.Label(processContainer, style="light", text="Process Id", justify=CENTER)
        lblProcessId.grid(column=2, row=0, padx=(BORDER_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")

        cbbProcessId = ttk.Combobox(processContainer, style="light")
        cbbProcessId.grid(column=2, row=1, padx=(COLUMN_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")
        cbbProcessId.bind('<Button-1>', OnProcessIdClicked)
        cbbProcessId.bind('<<ComboboxSelected>>', OnProcessIdSelected)

        processContainer.grid(column=0, row=0, padx=(BORDER_SPACE, BORDER_SPACE), pady=(BORDER_SPACE, 0), sticky="nsew")
        # End process properties

        # Start function properties
        functionContainer = ttk.Frame(widgetsContainer)

        lblCallingConvention = ttk.Label(functionContainer, style="light", text="Calling Convention", justify=CENTER)
        lblCallingConvention.grid(column=0, row=0, padx=(BORDER_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")

        cbbCallingConvention = ttk.Combobox(functionContainer, style="light", values=self.eCallingConventions)
        cbbCallingConvention.grid(column=0, row=1, padx=(COLUMN_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")

        lblReturnType = ttk.Label(functionContainer, style="light", text="Return Type", justify=CENTER)
        lblReturnType.grid(column=1, row=0, padx=(BORDER_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")

        cbbReturnType = ttk.Combobox(functionContainer, style="light", values=self.eReturnTypes)
        cbbReturnType.grid(column=1, row=1, padx=(COLUMN_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")

        lblFunctionAdress = ttk.Label(functionContainer, style="light", text="Function Adress", justify=CENTER)
        lblFunctionAdress.grid(column=2, row=0, padx=(BORDER_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")

        cbbFunctionAdress = ttk.Combobox(functionContainer, style="light")
        cbbFunctionAdress.grid(column=2, row=1, padx=(COLUMN_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")
        cbbFunctionAdress.set("0x") # Function adress must start in hexadecimal format!
        cbbFunctionAdress.bind('<KeyRelease>', OnAdressWritten)

        lblModuleHandle = ttk.Label(functionContainer, style="light", text="Add Module Handle", justify=CENTER)
        lblModuleHandle.grid(column=3, row=0, padx=(BORDER_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")

        cbbModuleHandle = ttk.Combobox(functionContainer, style="light", values=self.eBooleanValues)
        cbbModuleHandle.grid(column=3, row=1, padx=(COLUMN_SPACE, COLUMN_SPACE), pady=(BORDER_SPACE, 0), sticky="n")

        functionContainer.grid(column=0, row=1, padx=(BORDER_SPACE, BORDER_SPACE), pady=(BORDER_SPACE, 0), sticky="nsew")
        # End function properties

        # Start function parameters properties
        paramsContainer = ttk.Notebook(widgetsContainer, style="info")
        paramsContainer.bind('<<NotebookTabChanged>>', AddOrRemoveParameter)

        paramsContainerInternal = ttk.Frame(paramsContainer, style="dark")
        paramsContainer.add(paramsContainerInternal, text="List of Parameters")
        paramsContainerInternalAddy = ttk.Frame(paramsContainer, style="light")
        paramsContainer.add(paramsContainerInternalAddy, text="+")
        paramsContainerInternalRemo = ttk.Frame(paramsContainer, style="light")
        paramsContainer.add(paramsContainerInternalRemo, text="-")

        paramsContainer.grid(column=0, row=2, padx=(BORDER_SPACE, BORDER_SPACE), pady=(BORDER_SPACE, 0), sticky="nsew")
        # End function parameters properties

        btnCallFunction = ttk.Button(widgetsContainer, style="info" , text="Execute the function in the target process", command=lambda:CallFunction(), padding=BORDER_SPACE)
        btnCallFunction.grid(column=0, row=3, padx=(BORDER_SPACE, BORDER_SPACE), pady=(BORDER_SPACE, 0), sticky="new")

        # We automatically add the first parameter, we don't use the event parameter
        AddOrRemoveParameter()

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
    MainWindow(app)
    app.mainloop()

if __name__ == "__main__":
    Main()