import pyinjector

def InjectDLL(procId, dllPath):
    return pyinjector.inject(procId, dllPath) != 0