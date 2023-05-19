#!/usr/bin/env python3

import os
import time
import signal
import sys
import random
import array as array
import pprint as p

def handler(signum, frame):
    # clear_screen()
    # restore_screen()
    os.system("stty echo")
    Screen.show_curser()
    sys.exit(0)

signal.signal(signal.SIGINT, handler)


canvas_w, canvas_h = os.get_terminal_size()
canvas_w -= 1
canvas_h -= 1

class Screen:
    def __init__(self):
        self.screen = [[' ' for x in range(canvas_w)] 
            for y in range(canvas_h)]

    def clear_screen():
        print("\x1b[1J", end='')
    
    def cursor(self, row, col, symbol):
        print(f"\x1b[{row};{col}H{symbol}", end='')
    
    def hide_curser():
        print(f"\x1b[?25l", end='')
    
    def show_curser():
        print(f"\x1b[?25h", end='')
    
    def fg_color(color = 70):
        print(f"\x1b[38;5;{color}m", end='')
    
    def save_screen():
        print(f"\1b[?47h", end='')
    
    def restore_screen():
        print(f"\1b[?47l", end='')
    
    def bold():
        print(f"\x1b[1m", end='')
    
    def unbold():
        print(f"\x1b[22m", end='')
            
    def dim():
        print(f"\x1b[2m", end='')


def random_char():
    result = ' '
    exclusions = [0x22,0x27,0x28,0x29,0x2c,0x2d,0x2e,0x2f,0x3a,0x3b,0x3c,0x3d,0x3e,0x5b,0x5c,0x5d,0x5e,0x5f,0x60,0x7b,0x7c,0x7d,0x7e]
    if (random.randrange(0,100) < 1):
        # Hangul
        result = random.randrange(0xAC00,0xD7AF)

    if (random.randrange(0,100) < 10):
        # Cyrillic
        result = random.randrange(0x400,0x4FF)
    
    elif (random.randrange(0,100) < 10):
        # Greek & Coptic
        result = random.randrange(0x370,0x3FF)
    
    elif (random.randrange(0,100) < 10):
        # Hebrew
        result = random.randrange(0x590,0x5FF)
    
    elif (random.randrange(0,100) < 10):
        # Runic
        result = random.randrange(0x16A0,0x16FF)
    
    else:
        # Latin
        result = random.randrange(0x21,0x7f)

    while (any(e == result for e in exclusions)): 
        result = random_char() 
    return result


# class Model_Old: 
#     def __init__(self):
#         self.fps       = 0
#         self.t         = self.fps
#         self.row       = 0
#         self.col       = 0
#         self.state_col = [0] * canvas_w
#         self.model     = [[' ' for x in range(canvas_w)] 
#                          for y in range(canvas_h)]
#
#     def tick(self):
#         t = random_char() 
#         if self.t == self.fps:
#             for i in range(canvas_w):
#                 self.row = self.state_col[self.col] % canvas_w 
#                 if random.randrange(0,100) < 20:
#                     self.model[self.row][self.col] = random_char()
#                     self.state_col[self.col] = (self.row + 1) % canvas_h
#                 else:
#                     self.model[self.row][self.col] = chr(0x20)
#     
#                 self.col = (self.col + 1) % len(self.model[0]) 
#         self.t = (self.t + 1) % (self.fps + 1)
#

class Text:
    def __init__(self, model, lifetime):
        self.x         = 0
        self.fps       = 1 
        self.lifetime  = lifetime 
        self.fps_count = self.fps
        self.model = model

    def tick(self, col = 1, delay = 0):
        # if delay % 1 == 0:
        d = delay + self.fps_count
        if 0 == d:
            self.model[self.x][col].char = chr(random_char())
            self.model[self.x][col].lifetime = self.lifetime - d
            # if random.randrange(0,100) < 90:
            #     self.model[self.x][col].lifetime = self.lifetime - 50
            self.x = (self.x + 1) % len(self.model) 
        self.decay(col)
        self.fps_count = (self.fps_count + col) % (self.fps+1) 

    def decay(self, col):
       for x in range(len(self.model)):
            self.model[x][col].lifetime -= 1
       # if self.model[x][y].lifetime == 1:
       #     Screen.fg_color(16)
       # elif self.model[x][y].lifetime == 2:
       #     Screen.fg_color(22)
            if self.model[x][col].lifetime <= 0:
                self.model[x][col].char = ' '

class Model_Data:
    def __init__(self, lifetime):
        self.lifetime = lifetime
        self.char = ' '


class Model:
    def __init__(self):
        self.lifetime = 650 
        self.model     = [[Model_Data(self.lifetime) for _ in range(canvas_w)] for _ in range(canvas_h * 2)]
        # self.t = [Text(self.model)] * canvas_w
        self.t = []
        for x in range(len(self.model[0])):
            self.t.append(Text(self.model, self.lifetime))


    def tick(self):
        for x in range(len(self.model[0])):
            self.t[x].tick(col=x, delay=random.randrange(0,14))
        


def main():
    FPS256  = 0.0039
    FPS128  = 0.0078
    FPS60   = 0.0166
    FPS30   = 0.0333
    model   = Model()
    screen  = Screen()

    Screen.clear_screen()
    Screen.hide_curser()
    os.system("stty -echo")
    Screen.fg_color()
    Screen.bold()

    greeting = " L o a d i n g   M a t r i x . . . ."
    greeting2 = " H e l l o     N e o ."
    for key, letter in enumerate(greeting):
        model.model[canvas_h][key].char = letter

    while (True):
        model.tick()
        # p.pprint(model.model)
        for col in range(0,canvas_h//1):
            for row in range(1,canvas_w//1,2):
                if model.model[col+canvas_h][row].char != screen.screen[col][row]:
                    print("")
                    screen.screen[col][row] = model.model[col+canvas_h][row].char
                    screen.cursor(col, row, screen.screen[col][row])

        time.sleep(0.0019)
 


if __name__ == '__main__':
    main()
