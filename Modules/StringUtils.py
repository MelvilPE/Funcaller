import sys
import re

REGEX_HEX_PATTERN = r'^0x[0-9A-Fa-f]+$'

def IsWideString(input):
    for char in input:
        if ord(char) > 0xFF:
            return True
    return False

def IsNoneOrEmpty(input):
    return ((input is None) or (input == ""))

def ConvertSafelyToInt(input):
    try:
        if re.match(REGEX_HEX_PATTERN, input):
            return int(input, 16)
    except:
        pass
    try:
        return int(input)
    except:
        pass

    return -1

def ConvertSafelyToBoolean(input):
    inputLower = input.lower()
    if inputLower == "0" or inputLower == "false":
        return False
    
    if inputLower == "1" or inputLower == "true":
        return True
    
    return False
