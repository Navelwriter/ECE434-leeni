#//////////////////////////////////////
# Noah Lee 
# ECE 434 hw01: Etch-a-sketch
# 12/04/2023
#//////////////////////////////////////

#!/usr/bin/env python3
#chmod +x etch.py

# import argparse
import curses

class Board:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        #create 2d array of size x*y, fill with "." to represent empty spaces
        self.board = [["." for i in range(self.x)] for j in range(self.x)]
        self.cursor = [0,0]
        self.shape = "X"
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
        stdscr.refresh()
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
    stdscr.addstr("\nYou have selected a board size of size (" + str(board.x) + " by " + str(board.y) + ")\n")
    stdscr.addstr("Press arrow keys to move the cursor, press 'c' to clear the screen, press 'f' to change cursor shape, and press 'q' to quit\n")
    stdscr.addstr("Press any key to continue")
    curses.noecho()
    stdscr.getkey()
    return board
        
def main(stdscr):
    board = startup(stdscr)
    board.clear(stdscr)
    while(True):
        board.draw(stdscr)
        c = stdscr.getkey()
        if c == 'q':
            break
        elif c == 'f':
            board.change_cursor(stdscr)
        elif c == 'c':
            board.clear(stdscr)
        elif c == 'KEY_UP':
            board.move('UP')
        elif c == 'KEY_DOWN':
            board.move('DOWN')
        elif c == 'KEY_LEFT':
            board.move('LEFT')
        elif c == 'KEY_RIGHT':
            board.move('RIGHT')
    



curses.wrapper(main)