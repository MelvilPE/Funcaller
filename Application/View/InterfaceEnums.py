import sys, os
sys.path.insert(0, os.path.abspath("."))

import View.InterfaceConsts as InterfaceConsts

eProgramArchitectures = [
    InterfaceConsts.ARCHITECTURE_X86,
    InterfaceConsts.ARCHITECTURE_X64
]

eBooleanValues = [
    InterfaceConsts.BOOL_TRUE,
    InterfaceConsts.BOOL_FALSE
]

eParameterTypes = [
    InterfaceConsts.TYPENAME_STD_STRING,
    InterfaceConsts.TYPENAME_CONST_CHAR_PTR,
    InterfaceConsts.TYPENAME_BOOLEAN,
    InterfaceConsts.TYPENAME_UINT8,
    InterfaceConsts.TYPENAME_UINT16,
    InterfaceConsts.TYPENAME_UINT32,
    InterfaceConsts.TYPENAME_UINT64
]

eReturnTypes = [InterfaceConsts.TYPENAME_VOID] + eParameterTypes

eCallingConventions = [
    InterfaceConsts.CONVENTION_CDECL,
    InterfaceConsts.CONVENTION_STDCALL,
    InterfaceConsts.CONVENTION_FASTCALL,
    InterfaceConsts.CONVENTION_THISCALL,
    InterfaceConsts.CONVENTION_VECTORCALL
]