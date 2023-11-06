import sys, os
sys.path.insert(0, os.path.abspath("."))

import Main
import Utilities.ProcessUtils as ProcessUtils
import View.InterfaceConsts as InterfaceConsts

HARDCODED_COMMAND = f'MSBuild.exe "{Main.SCRIPT_ROOT}" /p:Configuration=Debug /p:Platform=x86'


def BuildSolution(architecture):
    resultArchive = {'dllPath': '', 'errorMessage': ''}

    commandExecuted = HARDCODED_COMMAND

    if architecture == InterfaceConsts.ARCHITECTURE_X64:
        commandExecuted = commandExecuted.replace(InterfaceConsts.ARCHITECTURE_X86, InterfaceConsts.ARCHITECTURE_X64)

    if not Main.SCRIPT_ROOT.endswith("\\Application"):
        resultArchive['errorMessage'] = "MSBuild::BuildSolution failed to recognize where is located the main root path!"
        return resultArchive

    internalProjectDirectory = Main.SCRIPT_ROOT.replace("\\Application", f"\\{Main.INTERNAL_PROJECT_NAME}")
    internalProjectSolution = f"{internalProjectDirectory}\\{Main.INTERNAL_PROJECT_NAME}.sln"

    internalProjectBuildFile = internalProjectDirectory
    if architecture == InterfaceConsts.ARCHITECTURE_X86:
        internalProjectBuildFile += f"\\Debug\\{Main.INTERNAL_PROJECT_NAME}" 
    else:
        internalProjectBuildFile += f"\\{InterfaceConsts.ARCHITECTURE_X64}\\Debug\\{Main.INTERNAL_PROJECT_NAME}" 
    internalProjectBuildFile += ".dll"

    commandExecuted = commandExecuted.replace(Main.SCRIPT_ROOT, internalProjectSolution, 1)

    if not ProcessUtils.RunCommandSystem(commandExecuted):
        resultArchive['errorMessage'] = f"MSBuild::BuildSolution failed to run MSBuild command: {commandExecuted}"
        return resultArchive

    if not os.path.exists(internalProjectBuildFile):
        resultArchive['errorMessage'] = f"MSBuild::BuildSolution MSBuild command failed, as DLL file is missing at: {internalProjectBuildFile}"
        return resultArchive

    resultArchive['dllPath'] = internalProjectBuildFile
    return resultArchive

def UnitTests():
    BuildSolution(InterfaceConsts.ARCHITECTURE_X64)

if __name__ == "__main__":
    UnitTests()