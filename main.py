#!/usr/bin/env python3

import os
import time
import signal
import sys
import random
import array as array

def handler(signum, frame):
    # clear_screen()
    restore_screen()
    os.system("stty echo")
    show_curser()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)


canvas_w, canvas_h = os.get_terminal_size()

def clear_screen():
    print("\x1b[1J")

def cursor(row, col, symbol):
    print(f"\x1b[{row};{col}H{symbol}")

def hide_curser():
    print(f"\x1b[?25l")

def show_curser():
    print(f"\x1b[?25h")

def fg_color(color = 70):
    print(f"\x1b[38;5;{color}m")

def save_screen():
    print(f"\1b[?47h")

def restore_screen():
    print(f"\1b[?47l")

def bold():
    print(f"\x1b[1m")

def unbold():
    print(f"\x1b[22m")
        
def dim():
    print(f"\x1b[2m")

def char_set():
    # if (random.randrange(0,100) < 1):
    #     # Hangul
    #     return random.randrange(0xAC00,0xD7AF)

    # if (random.randrange(0,100) < 10):
    #     # Cyrillic
    #     return random.randrange(0x400,0x4FF)
    #
    # elif (random.randrange(0,100) < 10):
    #     # Greek & Coptic
    #     return random.randrange(0x370,0x3FF)
    #
    # elif (random.randrange(0,100) < 10):
    #     # Hebrew
    #     return random.randrange(0x590,0x5FF)
    #
    # elif (random.randrange(0,100) < 10):
    #     # Runic
    #     return random.randrange(0x16A0,0x16FF)
    #
    # else:
        # Latin
        return random.randrange(0x21,0x7f)


col_state = [0] * canvas_w 
exclusions = [0x22,0x27,0x28,0x29,0x2c,0x2d,0x2e,0x2f,0x3a,0x3b,0x3c,0x3d,0x3e,0x5b,0x5c,0x5d,0x5e,0x5f,0x60,0x7b,0x7c,0x7d,0x7e]

def draw_row(col, something):
    row = col_state[col] % canvas_h 
    t = char_set() 

    while (any(elem == t for elem in exclusions)): 
        t = char_set() 

    seed = random.randrange(0,100)
    if (seed < 10 and something[col] == 0):
        #cursor(row, col, t[random.randrange(0,len(t))])
        # cursor(row, col, chr(t))
        cursor(row, col, chr(t))
        col_state[col] = row + 1
    # elif (seed < 10 and something[col] == 1):
    #     cursor(row, col, chr(0x20))
    #     col_state[col] = row + 1
    else:
        cursor(row, col, chr(0x20))
        # col_state[col] = row + 1


def main():
    save_screen()
    clear_screen()
    hide_curser()
    os.system("stty -echo")
    fg_color()
    bold()
    
    while (True):
        something = [random.randrange(0,2) for x in range(0,canvas_w)]
        for col in range(0,canvas_h):
            # col_state = [0] * canvas_w 
            for row in range(0,canvas_w, 2):
                draw_row(row, something)
                time.sleep(0.0002)
                



if __name__ == '__main__':
    main()
