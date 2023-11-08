import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip

import sys, os
sys.path.insert(0, os.path.abspath("."))

import View.InterfaceEnums as InterfaceEnums
import View.InterfaceConsts as InterfaceConsts
import Model.InterfaceModel as InterfaceModel

import Utilities.ProcessUtils as ProcessUtils
import Utilities.MSBuild as MSBuild
import Utilities.DLLInjector as DLLInjector
import Utilities.StringUtils as StringUtils

import ctypes
import re

""" User Action Control with InterfaceView """

# Prevent the ability to switch tabs on the targeted widget
def AntiSwitchNotebook(notebook, tabIndex = 0) -> None:
    notebook.select(tabIndex)

# Brief functions to use the different tabs to add or remove parameters
def AddOrRemoveParameter(event, instanceMainWindow, addFirstParam = False) -> None:
    currTabIndex = 0
    if addFirstParam == True:
        currTabIndex = 1
    else:
        currTabIndex = instanceMainWindow.paramsContainer.index("current")
    if currTabIndex != 0:
        TAB_INDEX_ADDBTN = 1
        TAB_INDEX_REMBTN = 2
        # The action of the + button
        # We add a new parameter line
        if currTabIndex == TAB_INDEX_ADDBTN:
            if instanceMainWindow.numberOfParameters >= 10:
                ctypes.windll.user32.MessageBoxW(0, "MainGUI::AddOrRemoveParameter Currently impossible to add more than 10 parameters", "Funcaller", 16)
            else:
                parameterLine = ttk.Frame(instanceMainWindow.paramsContainerInternal, style="light")
                if addFirstParam == True:
                    ToolTip(parameterLine, bootstyle=(DANGER, INVERSE), text="Note that the first parameter is empty by default, which means that the function that you are trying to call has no input parameters")

                def OnParameterTypeSelected(event) -> None:
                    selectedIndex = cbbParamType.current()
                    parameterType = InterfaceEnums.eParameterTypes[selectedIndex]
                    cbbParamValue["values"] = []
                    if parameterType == InterfaceConsts.TYPENAME_STD_STRING:
                        cbbParamValue.set("")
                    elif parameterType == InterfaceConsts.TYPENAME_CONST_CHAR_PTR:
                        cbbParamValue.set("")
                    elif parameterType == InterfaceConsts.TYPENAME_BOOLEAN:
                        cbbParamValue["values"] = InterfaceEnums.eBooleanValues
                        cbbParamValue.set(InterfaceEnums.eBooleanValues[0])
                    elif parameterType == InterfaceConsts.TYPENAME_UINT8:
                        cbbParamValue.set("0x")
                    elif parameterType == InterfaceConsts.TYPENAME_UINT16:
                        cbbParamValue.set("0x")
                    elif parameterType == InterfaceConsts.TYPENAME_UINT32:
                        cbbParamValue.set("0x")
                    elif parameterType == InterfaceConsts.TYPENAME_UINT64:
                        cbbParamValue.set("0x")
                    return
                
                def OnParameterValueWritten(event) -> None:
                    parameterType = cbbParamType.get()
                    parameterValue = cbbParamValue.get()
                    if parameterType not in InterfaceEnums.eParameterTypes:
                        cbbParamValue.set("")
                        ctypes.windll.user32.MessageBoxW(0, "MainGUI::OnParameterValueWritten Parameter type is wrong!", "Funcaller", 16)
                        return
                    
                    if parameterType == InterfaceConsts.TYPENAME_STD_STRING and StringUtils.IsWideString(parameterValue):
                        cbbParamValue.set("")
                        ctypes.windll.user32.MessageBoxW(0, f"MainGUI::OnParameterValueWritten Wide strings for {InterfaceConsts.TYPENAME_STD_STRING} aren't supported!", "Funcaller", 16)
                        return

                    if parameterType == InterfaceConsts.TYPENAME_CONST_CHAR_PTR and StringUtils.IsWideString(parameterValue):
                        cbbParamValue.set("")
                        ctypes.windll.user32.MessageBoxW(0, f"MainGUI::OnParameterValueWritten Wide strings for {InterfaceConsts.TYPENAME_CONST_CHAR_PTR} aren't supported!", "Funcaller", 16)
                        return
                    
                    if parameterType == InterfaceConsts.TYPENAME_BOOLEAN and parameterValue not in InterfaceEnums.eBooleanValues:
                        cbbParamValue.set(InterfaceEnums.eBooleanValues[0])
                        ctypes.windll.user32.MessageBoxW(0, f"MainGUI::OnParameterValueWritten Value is not of type {InterfaceConsts.TYPENAME_BOOLEAN}!", "Funcaller", 16)
                        return

                    if parameterType == InterfaceConsts.TYPENAME_UINT8:
                        if not re.match(InterfaceConsts.HEX_FORMAT_REGEX, parameterValue) and parameterValue != "0x" or len(parameterValue) > len("0xFF"):
                            cbbParamValue.set("0x")
                            ctypes.windll.user32.MessageBoxW(0, f"MainGUI::OnParameterValueWritten {InterfaceConsts.TYPENAME_UINT8} value must be in hexadecimal format and size must be smaller than '0xFF'", "Funcaller", 16)
                            return
                    
                    if parameterType == InterfaceConsts.TYPENAME_UINT16:
                        if not re.match(InterfaceConsts.HEX_FORMAT_REGEX, parameterValue) and parameterValue != "0x" or len(parameterValue) > len("0xFFFF"):
                            cbbParamValue.set("0x")
                            ctypes.windll.user32.MessageBoxW(0, f"MainGUI::OnParameterValueWritten {InterfaceConsts.TYPENAME_UINT16} value must be in hexadecimal format and size must be smaller than '0xFFFF'", "Funcaller", 16)
                            return
                        
                    if parameterType == InterfaceConsts.TYPENAME_UINT32:
                        if not re.match(InterfaceConsts.HEX_FORMAT_REGEX, parameterValue) and parameterValue != "0x" or len(parameterValue) > len("0xFFFFFFFF"):
                            cbbParamValue.set("0x")
                            ctypes.windll.user32.MessageBoxW(0, f"MainGUI::OnParameterValueWritten {InterfaceConsts.TYPENAME_UINT32} value must be in hexadecimal format and size must be smaller than '0xFFFFFFFF'", "Funcaller", 16)
                            return
                        
                    if parameterType == InterfaceConsts.TYPENAME_UINT64:
                        if not re.match(InterfaceConsts.HEX_FORMAT_REGEX, parameterValue) and parameterValue != "0x" or len(parameterValue) > len("0xFFFFFFFFFFFFFFFF"):
                            cbbParamValue.set("0x")
                            ctypes.windll.user32.MessageBoxW(0, f"MainGUI::OnParameterValueWritten {InterfaceConsts.TYPENAME_UINT64} value must be in hexadecimal format and size must be smaller than '0xFFFFFFFFFFFFFFFF'", "Funcaller", 16)
                            return

                cbbParamType = ttk.Combobox(parameterLine, style="light", width=48, values=InterfaceEnums.eParameterTypes)
                cbbParamType.grid(column=0, row=0)
                cbbParamType.bind('<<ComboboxSelected>>', OnParameterTypeSelected)
                
                cbbParamValue = ttk.Combobox(parameterLine, style="light", width=48)
                cbbParamValue.grid(column=1, row=0)
                cbbParamValue.bind('<KeyRelease>', OnParameterValueWritten)

                parameterLine.grid(column=0, row=instanceMainWindow.numberOfParameters, sticky="nsew")
                instanceMainWindow.parameterLines.append(parameterLine)
                instanceMainWindow.numberOfParameters += 1

        # The action of the - button
        # We remove the last parameter line
        elif currTabIndex == TAB_INDEX_REMBTN and instanceMainWindow.numberOfParameters > 1:
                instanceMainWindow.parameterLines[instanceMainWindow.numberOfParameters-1].grid_forget()
                instanceMainWindow.parameterLines.pop()
                instanceMainWindow.numberOfParameters -= 1
    
    # We prevent the tab change since they act like buttons
    AntiSwitchNotebook(instanceMainWindow.paramsContainer)

def SetProcInfosFromIndex(selectedProcessIndex, instanceMainWindow) -> None:
    instanceMainWindow.cbbProcessName.set(instanceMainWindow.processesList[selectedProcessIndex]["name"])
    instanceMainWindow.cbbProcessId.set(instanceMainWindow.processesList[selectedProcessIndex]["pid"])

def UpdateProcessesList(intanceMainWindow) -> None:
    intanceMainWindow.processesList = ProcessUtils.ListRunningProcesses()
    intanceMainWindow.cbbProcessName["values"] = ProcessUtils.ListProcessesNames(intanceMainWindow.processesList)
    intanceMainWindow.cbbProcessId["values"] = ProcessUtils.ListProcessesIds(intanceMainWindow.processesList)

def OnProcessNameClicked(event, instanceMainWindow) -> None:
    UpdateProcessesList(instanceMainWindow)

def OnProcessNameSelected(event, instanceMainWindow) -> None:
    selectedIndex = instanceMainWindow.cbbProcessName.current()
    SetProcInfosFromIndex(selectedIndex, instanceMainWindow)

def OnProcessIdClicked(event, instanceMainWindow) -> None:
    UpdateProcessesList(instanceMainWindow)

def OnProcessIdSelected(event, instanceMainWindow) -> None:
    selectedIndex = instanceMainWindow.cbbProcessId.current()
    SetProcInfosFromIndex(selectedIndex, instanceMainWindow)

def OnAdressWritten(event, instanceMainWindow) -> None:
    if instanceMainWindow.cbbArchitecture.get() not in InterfaceEnums.eProgramArchitectures:
        instanceMainWindow.cbbFunctionAdress.set("0x")
        ctypes.windll.user32.MessageBoxW(0, "InterfaceController::OnAdressWritten Before entering an address, please select an architecture", "Funcaller", 16)
        return

    if not re.match(InterfaceConsts.HEX_FORMAT_REGEX, instanceMainWindow.cbbFunctionAdress.get()) and instanceMainWindow.cbbFunctionAdress.get() != "0x":
        instanceMainWindow.cbbFunctionAdress.set("0x")
        ctypes.windll.user32.MessageBoxW(0, "InterfaceController::OnAdressWritten Function adress must be in hexadecimal format", "Funcaller", 16)
        return

    if instanceMainWindow.cbbArchitecture.get() == InterfaceConsts.ARCHITECTURE_X86 and len(instanceMainWindow.cbbFunctionAdress.get()) > len("0xFFFFFFFF"):
        instanceMainWindow.cbbFunctionAdress.set("0x")
        ctypes.windll.user32.MessageBoxW(0, f"InterfaceController::OnAdressWritten For {InterfaceConsts.ARCHITECTURE_X86} architecture, the address size must be smaller than '0xFFFFFFFF'.", "Funcaller", 16)
        return

    if instanceMainWindow.cbbArchitecture.get() == InterfaceConsts.ARCHITECTURE_X64 and len(instanceMainWindow.cbbFunctionAdress.get()) > len("0xFFFFFFFFFFFFFFFF"):
        instanceMainWindow.cbbFunctionAdress.set("0x")
        ctypes.windll.user32.MessageBoxW(0, f"InterfaceController::OnAdressWritten For {InterfaceConsts.ARCHITECTURE_X64} architecture, the address size must be smaller than '0xFFFFFFFFFFFFFFFF'.", "Funcaller", 16)
        return

""" User Action Control with InterfaceModel """

def InitializeCall(interfaceModelArchive):
    if len(interfaceModelArchive) == 0:
        return "InterfaceController::InitializeCall model can't be empty!"
    
    # Architecture
    if StringUtils.IsNoneOrEmpty(interfaceModelArchive['architecture']):
        return "InterfaceController::InitializeCall model has missing architecture!"
    
    if interfaceModelArchive['architecture'] not in InterfaceEnums.eProgramArchitectures:
        return "InterfaceController::InitializeCall model architecture is wrong!"
    
    # Process Name & Id
    processesList = ProcessUtils.ListRunningProcesses()
    if len(processesList) == 0:
        return "InterfaceController::InitializeCall Collected process list is empty!"
        
    if StringUtils.IsNoneOrEmpty(interfaceModelArchive['processName']):
        return "InterfaceController::InitializeCall model has missing process name!"
    
    foundProcessName = any(processArchive['name'] == interfaceModelArchive['processName'] for processArchive in processesList)
    if not foundProcessName:
        return "InterfaceController::InitializeCall Process name wasn't found in refreshed process list!"

    if interfaceModelArchive['processId'] is None:
        return "InterfaceController::InitializeCall model has missing process id!"
    
    foundProcessId = any(str(processArchive['pid']) == str(interfaceModelArchive['processId']) for processArchive in processesList)
    if not foundProcessId:
        return "InterfaceController::InitializeCall Process id wasn't found in refreshed process list!"
    
    # Calling Convention
    if StringUtils.IsNoneOrEmpty(interfaceModelArchive['callingConvention']):
        return "InterfaceController::InitializeCall model has missing calling convention!"
    
    if interfaceModelArchive['callingConvention'] not in InterfaceEnums.eCallingConventions:
        return "InterfaceController::InitializeCall model calling convention is wrong!"
    
    # Return Type
    if StringUtils.IsNoneOrEmpty(interfaceModelArchive['returnType']):
        return "InterfaceController::InitializeCall model has missing return type!"
    
    if interfaceModelArchive['returnType'] not in InterfaceEnums.eReturnTypes:
        return "InterfaceController::InitializeCall model return type is wrong!"
    
    # Function Adress
    if interfaceModelArchive['functionAdress'] is None:
        return "InterfaceController::InitializeCall model has missing function adress!"
    
    if interfaceModelArchive['functionAdress'] == 0 or interfaceModelArchive['functionAdress'] == -1:
        return "InterfaceController::InitializeCall model function adress is wrong!"
    
    # Module Handle
    if interfaceModelArchive['moduleHandle'] is None:
        return "InterfaceController::InitializeCall model has missing module handle boolean value!"
    
    # Serializing model file
    if not InterfaceModel.Serialize(interfaceModelArchive):
        return "InterfaceController::InitializeCall saving model file has failed!"

    # Injecting model file if MSBuild is successfull
    solutionResult = MSBuild.BuildSolution(interfaceModelArchive['architecture'])
    if solutionResult['dllPath'] == '':
        return solutionResult['errorMessage']
    
    buildedDLL = solutionResult['dllPath']
    if not DLLInjector.InjectDLL(int(interfaceModelArchive['processId']), buildedDLL):
        return "InterfaceController::InitializeCall DLL injection has failed after build!"

    return ""
