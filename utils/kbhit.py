import sys
from select import select

def kbhit():
    dr,dw,de = select([sys.stdin], [], [], 0)
    return dr != []
def getch():
    try:
        ch = sys.stdin.read(1)
        if ch == '':
            return
    finally:
        return ch

def getstr(len):
    return sys.stdin.read(len)