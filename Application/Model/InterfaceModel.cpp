#include "InterfaceModel.h"

void InterfaceModel::ExecutePlaceHolder()
{
    uint64_t functionAdressCalculated = static_cast<uint64_t>(functionAdressHolder);

    MODULEINFO moduleInfo = ProcessUtils::GetModuleInfo();
    uintptr_t baseAdress = reinterpret_cast<uintptr_t>(moduleInfo.lpBaseOfDll);
    uintptr_t moduleSize = static_cast<uintptr_t>(moduleInfo.SizeOfImage);

	if (functionAdressCalculated > (baseAdress + moduleSize))
    {
        MessageBox(NULL, "InterfaceController::TryCallingFunction failed to call function, function adress can't be bigger than base adress + module size!", "Funcaller", 16);
		return;
    }

    if (functionAdressCalculated < baseAdress)
    {
        functionAdressCalculated += baseAdress;
        if (functionAdressCalculated < baseAdress)
        {
            MessageBox(NULL, "InterfaceController::TryCallingFunction failed to call function, function adress is smaller than base adress after adding module handle!", "Funcaller", 16);
		    return;
        }
    }

	typedef returnTypeHolder(callingConventionHolder* _CalledFunction)(parametersLinesHolder);
	_CalledFunction CalledFunction = (_CalledFunction)(static_cast<uintptr_t>(functionAdressCalculated));
	CalledFunction(parametersReadyHolder);
}