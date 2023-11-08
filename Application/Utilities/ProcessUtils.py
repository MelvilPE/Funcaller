import subprocess
import psutil
import ctypes
import os

def ListRunningProcesses() -> list:
    processesList = []
    for process in psutil.process_iter(attrs=['name', 'pid']):
        try:
            if process.info['name'] != None and process.info['name'] != "":
                process_dict = {'name': process.info['name'], 'pid': process.info['pid']}
                processesList.append(process_dict)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processesList

def ListProcessesNames(processesList) -> list:
    return [process['name'] for process in processesList]

def ListProcessesIds(processesList) -> list:
    return [process['pid'] for process in processesList]

def RunCommandSystem(command):
    return os.system(command) == 0