import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip

import View.InterfaceEnums as InterfaceEnums
import View.InterfaceConsts as InterfaceConsts
import Controller.InterfaceController as InterfaceController

import Utilities.ProcessUtils as ProcessUtils
import Utilities.StringUtils as StringUtils

import ctypes
import re

# Brief class to manage the application GUI & ACTIONS
class MainWindow(ttk.Frame):
    def __init__(self, master) -> None:
        self.windowContainer = None
        self.widgetsContainer = None
        self.processContainer = None
        self.lblArchitecture = None
        self.cbbArchitecture = None
        self.lblProcessName = None
        self.cbbProcessName = None
        self.lblProcessId = None
        self.cbbProcessId = None
        self.functionContainer = None
        self.lblCallingConvention = None
        self.cbbCallingConvention = None
        self.lblReturnType = None
        self.cbbReturnType = None
        self.lblFunctionAdress = None
        self.cbbFunctionAdress = None
        self.lblModuleHandle = None
        self.cbbModuleHandle = None
        self.paramsContainer = None
        self.btnFinalCalledFunction = None

        self.numberOfParameters = 0
        self.parameterLines = []
        self.processesList = []
        self.InitializeInterface(master)

    # Brief function for initializing interface
    def InitializeInterface(self, master) -> None:
        def CollectParameterLinesFromInterface() -> list:
            dumpedParameters = []
            for lineIndex in range(len(self.parameterLines)):
                childrenWidgets = self.parameterLines[lineIndex].winfo_children()
                keyTypes = childrenWidgets[0].get()
                keyValue = childrenWidgets[1].get()
                if keyTypes not in InterfaceEnums.eParameterTypes:
                    continue

                # Here we convert informations to correct type
                receivedParameter = {}
                if keyTypes == "String(const char*)":
                    receivedParameter[keyTypes] = keyValue
                if keyTypes == "Bool":
                    if keyValue in InterfaceEnums.eBooleanValues or keyValue == 0 or keyValue == 1:
                        receivedParameter[keyTypes] = StringUtils.ConvertSafelyToBoolean(keyValue)
                if keyTypes == "Byte":
                    if StringUtils.ConvertSafelyToInt(keyValue) != -1:
                        receivedParameter[keyTypes] = StringUtils.ConvertSafelyToInt(keyValue)
                if keyTypes == "Word":
                    if StringUtils.ConvertSafelyToInt(keyValue) != -1:
                        receivedParameter[keyTypes] = StringUtils.ConvertSafelyToInt(keyValue)
                if keyTypes == "Dword":
                    if StringUtils.ConvertSafelyToInt(keyValue) != -1:
                        receivedParameter[keyTypes] = StringUtils.ConvertSafelyToInt(keyValue)
                if keyTypes == "Qword":
                    if StringUtils.ConvertSafelyToInt(keyValue) != -1:
                        receivedParameter[keyTypes] = StringUtils.ConvertSafelyToInt(keyValue)
                # We can skip if key types condition has not been declared here or value is wrong
                if len(receivedParameter) == 0:
                    continue

                dumpedParameters.append(receivedParameter)
            return dumpedParameters

        def CollectArchiveFromInterface() -> dict:
            collectedArchive = {}
            collectedArchive["architecture"] = self.cbbArchitecture.get()
            collectedArchive["processName"] = self.cbbProcessName.get()
            collectedArchive["processId"] = StringUtils.ConvertSafelyToInt(self.cbbProcessId.get())
            collectedArchive["callingConvention"] = self.cbbCallingConvention.get()
            collectedArchive["returnType"] = self.cbbReturnType.get()
            collectedArchive["functionAdress"] = StringUtils.ConvertSafelyToInt(self.cbbFunctionAdress.get())
            collectedArchive["moduleHandle"] = StringUtils.ConvertSafelyToBoolean(self.cbbModuleHandle.get())
            collectedArchive["parameterLines"] = CollectParameterLinesFromInterface()
            return collectedArchive

        def FinalCalledFunction() -> None:
            resultArchive = CollectArchiveFromInterface()
            strValidation = InterfaceController.SaveInterfaceModelArchive(resultArchive)
            if not StringUtils.IsNoneOrEmpty(strValidation):
                ctypes.windll.user32.MessageBoxW(0, strValidation, "Funcaller", 16)
                return False
            # TODO: Inject a dll into the target process

        super().__init__(master)
        self.grid(column=0, row=0, sticky="nsew")

        # Creation of the main window container
        self.windowContainer = ttk.Frame(self)
        self.windowContainer.grid(column=0, row=0, sticky="nsew")

        # Creation of the container for every widgets
        self.widgetsContainer = ttk.Frame(self.windowContainer)
        self.widgetsContainer.grid(column=0, row=0, sticky="nsew")

        # Start process properties
        self.processContainer = ttk.Frame(self.widgetsContainer)

        self.lblArchitecture = ttk.Label(self.processContainer, style="light", text="Program Architecture", justify=CENTER)
        self.lblArchitecture.grid(column=0, row=0, padx=(InterfaceConsts.BORDER_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")

        self.cbbArchitecture = ttk.Combobox(self.processContainer, style="light", values=InterfaceEnums.eProgramArchitectures)
        self.cbbArchitecture.grid(column=0, row=1, padx=(InterfaceConsts.COLUMN_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")

        self.lblProcessName = ttk.Label(self.processContainer, style="light", text="Process Name", justify=CENTER)
        self.lblProcessName.grid(column=1, row=0, padx=(InterfaceConsts.BORDER_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")

        self.cbbProcessName = ttk.Combobox(self.processContainer, style="light")
        self.cbbProcessName.grid(column=1, row=1, padx=(InterfaceConsts.COLUMN_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")
        self.cbbProcessName.bind('<Button-1>', lambda event: InterfaceController.OnProcessNameClicked(event, self))
        self.cbbProcessName.bind('<<ComboboxSelected>>', lambda event: InterfaceController.OnProcessNameSelected(event, self))

        self.lblProcessId = ttk.Label(self.processContainer, style="light", text="Process Id", justify=CENTER)
        self.lblProcessId.grid(column=2, row=0, padx=(InterfaceConsts.BORDER_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")

        self.cbbProcessId = ttk.Combobox(self.processContainer, style="light")
        self.cbbProcessId.grid(column=2, row=1, padx=(InterfaceConsts.COLUMN_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")
        self.cbbProcessId.bind('<Button-1>', lambda event: InterfaceController.OnProcessIdClicked(event, self))
        self.cbbProcessId.bind('<<ComboboxSelected>>', lambda event: InterfaceController.OnProcessIdSelected(event, self))

        self.processContainer.grid(column=0, row=0, padx=(InterfaceConsts.BORDER_SPACE, InterfaceConsts.BORDER_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="nsew")
        # End process properties

        # Start function properties
        self.functionContainer = ttk.Frame(self.widgetsContainer)

        self.lblCallingConvention = ttk.Label(self.functionContainer, style="light", text="Calling Convention", justify=CENTER)
        self.lblCallingConvention.grid(column=0, row=0, padx=(InterfaceConsts.BORDER_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")

        self.cbbCallingConvention = ttk.Combobox(self.functionContainer, style="light", values=InterfaceEnums.eCallingConventions)
        self.cbbCallingConvention.grid(column=0, row=1, padx=(InterfaceConsts.COLUMN_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")

        self.lblReturnType = ttk.Label(self.functionContainer, style="light", text="Return Type", justify=CENTER)
        self.lblReturnType.grid(column=1, row=0, padx=(InterfaceConsts.BORDER_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")

        self.cbbReturnType = ttk.Combobox(self.functionContainer, style="light", values=InterfaceEnums.eReturnTypes)
        self.cbbReturnType.grid(column=1, row=1, padx=(InterfaceConsts.COLUMN_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")

        self.lblFunctionAdress = ttk.Label(self.functionContainer, style="light", text="Function Adress", justify=CENTER)
        self.lblFunctionAdress.grid(column=2, row=0, padx=(InterfaceConsts.BORDER_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")

        self.cbbFunctionAdress = ttk.Combobox(self.functionContainer, style="light")
        self.cbbFunctionAdress.grid(column=2, row=1, padx=(InterfaceConsts.COLUMN_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")
        self.cbbFunctionAdress.set("0x") # Function adress must start in hexadecimal format!
        self.cbbFunctionAdress.bind('<KeyRelease>', lambda event: InterfaceController.OnAdressWritten(event, self))

        self.lblModuleHandle = ttk.Label(self.functionContainer, style="light", text="Add Module Handle", justify=CENTER)
        self.lblModuleHandle.grid(column=3, row=0, padx=(InterfaceConsts.BORDER_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")

        self.cbbModuleHandle = ttk.Combobox(self.functionContainer, style="light", values=InterfaceEnums.eBooleanValues)
        self.cbbModuleHandle.grid(column=3, row=1, padx=(InterfaceConsts.COLUMN_SPACE, InterfaceConsts.COLUMN_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="n")

        self.functionContainer.grid(column=0, row=1, padx=(InterfaceConsts.BORDER_SPACE, InterfaceConsts.BORDER_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="nsew")
        # End function properties

        # Start function parameters properties
        self.paramsContainer = ttk.Notebook(self.widgetsContainer, style="info")
        self.paramsContainer.bind('<<NotebookTabChanged>>', lambda event: InterfaceController.AddOrRemoveParameter(None, self, False))

        self.paramsContainerInternal = ttk.Frame(self.paramsContainer, style="dark")
        self.paramsContainer.add(self.paramsContainerInternal, text="List of Parameters")
        self.paramsContainerInternalAddy = ttk.Frame(self.paramsContainer, style="light")
        self.paramsContainer.add(self.paramsContainerInternalAddy, text="+")
        self.paramsContainerInternalRemo = ttk.Frame(self.paramsContainer, style="light")
        self.paramsContainer.add(self.paramsContainerInternalRemo, text="-")

        self.paramsContainer.grid(column=0, row=2, padx=(InterfaceConsts.BORDER_SPACE, InterfaceConsts.BORDER_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="nsew")
        # End function parameters properties

        self.btnFinalCalledFunction = ttk.Button(self.widgetsContainer, style="info" , text="Execute the function in the target process", command=lambda:FinalCalledFunction(), padding=InterfaceConsts.BORDER_SPACE)
        self.btnFinalCalledFunction.grid(column=0, row=3, padx=(InterfaceConsts.BORDER_SPACE, InterfaceConsts.BORDER_SPACE), pady=(InterfaceConsts.BORDER_SPACE, 0), sticky="new")

        # We automatically add the first parameter, we don't use the event parameter
        InterfaceController.AddOrRemoveParameter(None, self, True)
