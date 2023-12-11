#//////////////////////////////////////
# Noah Lee 
# ECE 434 hw01: Etch-a-sketch
# 12/10/2023
#//////////////////////////////////////

#!/usr/bin/env python3
#chmod +x etch.py

# import argparse
import curses
import gpiod
import time

CONSUMER='getset'
CHIP='1'
getoffsets=[13, 12, 15, 14] # P8_11 P8_12 P8_15 P8_16
button_mapping=['UP','DOWN','LEFT','RIGHT']
combo_mapping=['CLEAR','TOGGLE','QUIT']




class Board:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #create 2d array of size x*y, fill with "." to represent empty spaces
        self.board = [["." for i in range(self.x)] for j in range(self.x)]
        self.cursor = [0,0]
        self.shape = "X"
        self.button_setup()

    def button_setup(self):
        chip = gpiod.Chip(CHIP)
        self.lines = chip.get_lines(getoffsets)
        self.lines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_RISING_EDGE)
        self.last_val = self.lines.get_values()

    def clear(self, stdscr):
        self.board = [["." for i in range(self.x)] for j in range(self.y)]
        stdscr.clear()

    def move(self, dir):
        if dir == 'UP':
            self.cursor[1] -= 1
        elif dir == 'DOWN':
            self.cursor[1] += 1
        elif dir == 'LEFT':
            self.cursor[0] -= 1
        elif dir == 'RIGHT':
            self.cursor[0] += 1

        if self.cursor[0] < 0:
            self.cursor[0] = 0
        elif self.cursor[0] >= self.x:
            self.cursor[0] = self.x - 1
        if self.cursor[1] < 0:
            self.cursor[1] = 0
        elif self.cursor[1] >= self.y:
            self.cursor[1] = self.y - 1
        
        self.board[self.cursor[1]][self.cursor[0]] = self.shape

    def draw(self, stdscr):
        #draw the board by printing each element of the 2d array
        #change the element at the cursor to "X" to represent the cursor
        stdscr.clear()
        #use a .join() to convert the existing 2d array into a string, this keeps the historical positions of the cursor and allows it to persist like an etch-a-sketch
        boardstr = "\n".join(["".join(row) for row in self.board])

        stdscr.addstr(boardstr)
        printInstructions(stdscr)
        stdscr.refresh()

    def toggle_cursor(self):
        if self.shape == "X":
            self.shape = "."
        else:
            self.shape = "X"

    def change_cursor(self,stdscr):
        #prompt user for a new cursor shape on the bottom of the screen like vim 
        curses.echo() #to allow user to see their input
        stdscr.addstr("Enter a new cursor shape:")
        input = stdscr.getstr()
        curses.noecho()
        #remove the prompt and the user input
        stdscr.move(self.y+1,0)
        stdscr.clrtoeol()
        #check if the input is valid, if not, do nothing
        if len(input) == 0:
            return

        #only get the first character of the input and cast to utf-8
        self.shape = input.decode('utf-8')[0]
        self.board[self.cursor[1]][self.cursor[0]] = self.shape
        self.draw(stdscr)

        
def startup(stdscr):
    stdscr.clear()
    curses.echo()
    curses.curs_set(0) #hide cursor
    stdscr.addstr("Welcome to Etch-a-Sketch by Noah Lee\n")
    stdscr.addstr("Please enter the x-size of the screen: ")
    board = Board(0,0)
    input = stdscr.getstr() #get input from user
    if input.isdigit() & (int(input) > 0) & (int(input) <= 80): #checks if input is valid, 0<x<30
        board.x = int(input)
    else:
        stdscr.addstr("\nInvalid input, x and y must be between (0,0) and (30,80), press any key to try again")
        stdscr.getkey() 
        startup(stdscr)

    stdscr.addstr("\nPlease enter the y-size of the screen: ")
    input = stdscr.getstr() #get input from user

    if input.isdigit() & (int(input) > 0) & (int(input) <= 30): #checks if input is valid, 0<y<30
        board.y = int(input)
    else:
        stdscr.addstr("\nInvalid input, x and y must be between (0,0) and (30,80), press any key to try again")
        stdscr.getkey() 
        startup(stdscr)
    #create board
    printInstructions(stdscr)
    stdscr.addstr("Press any key on keyboard to continue")
    curses.noecho()
    stdscr.getkey()
    return board
        
def main(stdscr):
    board = startup(stdscr)
    board.clear(stdscr)
    board.draw(stdscr)
    while(True):
        butt_in = board.lines.event_wait(sec=1) #wait for button press
        quit = 0
        if butt_in:
            butt = board.lines.get_values()
            for k in range(len(butt)):
                if(k < len(butt)-1):
                    if(butt[k]==1 & butt[k+1]==1): #checks if 2 buttons are pressed at same time
                        if combo_mapping[k] == "CLEAR":
                            board.clear(stdscr)
                            board.draw(stdscr)
                        elif combo_mapping[k] == "TOGGLE":
                            board.toggle_cursor()
                        elif combo_mapping[k] == "QUIT":
                            quit = 1
                            break

                if butt[k] != board.last_val[k]: #check if button is debounced
                    if butt[k]:                  #if button is pressed move
                        board.move(button_mapping[k])
                        board.draw(stdscr)
                    board.last_val[k] = butt[k]
        if quit:
            break
    
def printInstructions(stdscr):
    stdscr.addstr("\nButton 0: UP, Button 1: DOWN, Button 2: LEFT, Button 3: RIGHT\n")
    stdscr.addstr("Press Button 0 and Button 1 Simultaneously to CLEAR BOARD\n")
    stdscr.addstr("Press Button 1 and Button 2 Simultaneously to TOGGLE CURSOR TO DRAW OR ERASE\n")
    stdscr.addstr("Press Button 3 and Button 4 Simultaneously to QUIT\n")



curses.wrapper(main)