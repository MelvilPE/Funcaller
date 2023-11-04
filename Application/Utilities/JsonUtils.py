import json

def CreateFileFromArchive(dictArch, filePath):
    with open(filePath, "w") as jsonFile:
        try:
            json.dump(obj=dictArch, fp=jsonFile, indent=2)
        except:
            return False

    return True
