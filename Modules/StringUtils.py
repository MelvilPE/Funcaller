import sys

def IsWideString(input):
    for char in input:
        if ord(char) > 0xFF:
            return True
    return False