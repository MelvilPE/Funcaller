import json

def CreateFileFromDict(dictArch, filePath):
    with open(filePath, "w") as jsonFile:
        json.dump(obj=dictArch, fp=jsonFile, indent=2)
