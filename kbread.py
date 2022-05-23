import sys
import termios
from utils.kbhit import kbhit, getch

def ReadFromStream(show = True, maskingChar = '*'):
    strBuffer = ""
    fd = sys.stdin.fileno()
    new_term = termios.tcgetattr(fd)
    old_term = termios.tcgetattr(fd)

    # New terminal setting unbuffered
    new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)
    
    count = 0
    while True:
        if kbhit():
            c = getch()
            ord_c = ord(c)
                        
            if c == '\x1b': # ESC
                termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
                return ""
            
            if c == '\x7f' and count > 0:
                sys.stdout.write('\b \b')
                sys.stdout.flush()
                count -= 1
                strBuffer = strBuffer[:-1]
                continue
                
            if c == '\n':
                termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
                return strBuffer
        
            if(c != '\x7f'):    
                if(show == False):
                    strBuffer += c
                    count = count + 1
                    sys.stdout.write(maskingChar)
                    sys.stdout.flush()
                    continue
                
                strBuffer += c
                count = count + 1
                sys.stdout.write(c)
                sys.stdout.flush()
            
def getKey():
    fd = sys.stdin.fileno()
    new_term = termios.tcgetattr(fd)
    old_term = termios.tcgetattr(fd)

    # New terminal setting unbuffered
    new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)
    termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)
    
    if kbhit():
        c = getch()
        ord_c = ord(c)
        termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
        return c
    
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
    return ''

def GetArrowKey(results):
    fd = sys.stdin.fileno()
    new_term = termios.tcgetattr(fd)
    old_term = termios.tcgetattr(fd)

    # New terminal setting unbuffered
    new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)
    termios.tcsetattr(fd, termios.TCSANOW, new_term)

    if kbhit():
        result = ''
        second = ''
        first = getch()
        if first == '\x1b':
            second = getch()
            if second == '[':
                result = ord(getch())
        else:
            result = ord(first)
            
        if first == '\x1b' and result == 65: # 65 -> up
            results.append(first)
            results.append(result)
            termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
            return 1
        elif first == '\x1b' and result == 66: # 66 -> down
            results.append(first)
            results.append(result)
            termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
            return 2
        elif first == '\x1b' and result == 67: # 67 -> right
            results.append(first)
            results.append(result)
            termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
            return 3
        elif first == '\x1b' and result == 68: # 68 -> left
            results.append(first)
            results.append(result)
            termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
            return 4
        else:
            results.append(result)
            results.append('\0')
            termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
            return 0
    
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)