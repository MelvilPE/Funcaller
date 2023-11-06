#pragma once
#include "../Includes.h"

class ProcessUtils
{
public:
	static std::string GetProcessExePath();
	static std::string GetProcessExeDirectory();

	static std::string GetProcessName();
	static MODULEINFO GetModuleInfo();
};