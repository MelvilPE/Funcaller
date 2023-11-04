import sys, os
sys.path.insert(0, os.path.abspath("."))

import Utilities.JsonUtils as JsonUtils

# Listing of all InterfaceModel content and their specific types
"""
interfaceModelArchive['architecture'] -> type: str
interfaceModelArchive['processName'] -> type: str
interfaceModelArchive['processId'] -> type: int
interfaceModelArchive['callingConvention'] -> type: str
interfaceModelArchive['returnType'] -> type: str
interfaceModelArchive['functionAdress'] -> type: int
interfaceModelArchive['moduleHandle'] -> type: bool
interfaceModelArchive['parameterLines'] -> type: list[dict]
"""

JSON_MODEL_NAME = "InterfaceModel.json"
JSON_MODEL_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\" + JSON_MODEL_NAME

def Serialize(interfaceModelArchive, modelPath = None):
    if modelPath != None:
        return JsonUtils.CreateFileFromArchive(interfaceModelArchive, modelPath)
    else:
        return JsonUtils.CreateFileFromArchive(interfaceModelArchive, JSON_MODEL_PATH)
