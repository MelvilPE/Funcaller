#include "ProcessUtils.h"

std::string ProcessUtils::GetProcessExePath()
{
    WCHAR executablePathW[MAX_PATH];
    GetModuleFileNameW(NULL, executablePathW, MAX_PATH);

    std::wstring executablePathStrW(executablePathW);
    std::string executablePath = std::string(executablePathStrW.begin(), executablePathStrW.end());
    return executablePath;
}

std::string ProcessUtils::GetProcessExeDirectory()
{
    std::string executablePath = GetProcessExePath();
    std::filesystem::path executableFileSystemPath(executablePath);
    std::string executableDirectory = executableFileSystemPath.parent_path().string();
    return executableDirectory;
}

std::string ProcessUtils::GetProcessName()
{
	HMODULE hExe = GetModuleHandle(NULL);
	char fullPath[MAX_PATH]{ 0 };
	char fname[MAX_PATH] = { 0 };
	char ext[MAX_PATH] = { 0 };
	char procName[MAX_PATH] = { 0 };
	GetModuleFileName(hExe, fullPath, MAX_PATH);
	_splitpath(fullPath, 0, 0, fname, ext);
	strcpy(procName, fname);
	strcat(procName, ext);
	return std::string(procName);
}

MODULEINFO ProcessUtils::GetModuleInfo()
{
	MODULEINFO modInfo = { NULL };
	HMODULE hModule = GetModuleHandle(GetProcessName().c_str());
	if (hModule == NULL)
	{
		return modInfo;
	}

	GetModuleInformation(GetCurrentProcess(), hModule, &modInfo, sizeof(MODULEINFO));
	return modInfo;
}