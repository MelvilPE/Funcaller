import sys, os
sys.path.insert(0, os.path.abspath("."))

import Main
import View.InterfaceConsts as InterfaceConsts
# import Utilities.JsonUtils as JsonUtils

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

SCRIPT_NAME = os.path.basename(__file__)
SCRIPT_ROOT = os.path.dirname(__file__)
SCRIPT_PATH = __file__

CPP_MODEL_NAME = "InterfaceModel.cpp"
CPP_MODEL_PATH = SCRIPT_ROOT + "\\" + CPP_MODEL_NAME
CPP_MODEL_BUILD_PATH = Main.SCRIPT_ROOT.replace("\\Application", f"\\{Main.INTERNAL_PROJECT_NAME}\\Sources\\Internal\\Model\\{CPP_MODEL_NAME}")
CPP_MODEL_VALIDATOR = b"ExecutePlaceHolder()"

def Serialize(interfaceModelArchive, modelPath = None):
    if not os.path.isfile(CPP_MODEL_PATH) or os.path.getsize(CPP_MODEL_PATH) == 0:
        return False
    
    with open(CPP_MODEL_PATH, "rb") as orignalModelFile:
        originalFileData = orignalModelFile.read()

    if not CPP_MODEL_VALIDATOR in originalFileData:
        return False

    serializedFunctionAdress = interfaceModelArchive['functionAdress'].encode()
    serializedReturnType = interfaceModelArchive['returnType'].encode()
    serializedCallingConvention = interfaceModelArchive['callingConvention'].encode()

    serializedParametersLinesHolder = b""
    serializedParametersReadyHolder = b""

    receivedParameterLines = interfaceModelArchive['parameterLines']

    for parameterLineIndex, parameterLine in enumerate(receivedParameterLines):
        for keyType, valueArch in parameterLine.items():
            if parameterLineIndex != 0:
                serializedParametersLinesHolder += b", "
                serializedParametersReadyHolder += b", "

            serializedParametersLinesHolder += keyType.encode() + str(" param" + str(parameterLineIndex)).encode()

            if keyType == InterfaceConsts.TYPENAME_STD_STRING or keyType == InterfaceConsts.TYPENAME_CONST_CHAR_PTR:
                valueArch = '"' + valueArch + '"'

            serializedParametersReadyHolder += valueArch.encode()

    modifiedFileData = bytes(originalFileData)
    modifiedFileData = modifiedFileData.replace(b"functionAdressHolder", serializedFunctionAdress)
    modifiedFileData = modifiedFileData.replace(b"returnTypeHolder", serializedReturnType)
    modifiedFileData = modifiedFileData.replace(b"callingConventionHolder", serializedCallingConvention)
    modifiedFileData = modifiedFileData.replace(b"parametersLinesHolder", serializedParametersLinesHolder)
    modifiedFileData = modifiedFileData.replace(b"parametersReadyHolder", serializedParametersReadyHolder)
    
    if modelPath == None:
        modelPath = CPP_MODEL_BUILD_PATH
    try:
        with open(modelPath, "wb") as serializedFile:
            serializedFile.write(modifiedFileData)
    except:
        return False

    return True
