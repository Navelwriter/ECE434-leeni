#!/usr/bin/env python3

#//////////////////////////////////////
# Noah Lee 
# ECE 434 hw04: Etch-a-sketch w/ Flask
# 1/9/2024
#//////////////////////////////////////

#chmod +x etch.py

# import argparse
import smbus
import gpiod
import time
import sys
from flask import Flask, render_template, request

app = Flask(__name__)
bus = smbus.SMBus(2)
leftTMP = 0x49
rightTMP = 0x4A

offset = 5
GREEN = 0
RED = 1
debounce = 0
board = None
class Board:
    def __init__(self):
        self.x = 7
        self.y = 7
        self.out = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]        
        self.cursor = [0,0]
        self.left_old = 0
        self.right_old = 0
        self.color = GREEN
        self.baseTemp = self.get_temp()
        self.currTemp = self.get_temp()
        self.tempDebounce = 0
        self.display_setup()
        self.draw()
    
    def compare_temp(self):
        self.currTemp = self.get_temp() 
        if(self.currTemp[0] == (self.baseTemp[0]+2) and self.tempDebounce == 0): #compare the current temp to the baseline, temp increases by 2 when touched
            self.tempDebounce = 1 #This is part of debouncing
            if self.color == GREEN:
                self.color = RED
            else:
                self.color = GREEN
        if(self.currTemp[1] == (self.baseTemp[1]+2)):
            self.clear()
        if((self.currTemp[0] <= self.baseTemp[0]+1) and self.tempDebounce == 1): #Checks if it is currently being pressed, resets if temp dips down
            self.tempDebounce = 0

    def toggle_color(self):
        #toggle color
        if self.color == GREEN:
            self.color = RED
        else:
            self.color = GREEN

    def get_temp(self):
        temp1 = bus.read_byte_data(leftTMP, 0)
        temp2 = bus.read_byte_data(rightTMP, 0)
        return [temp1,temp2]

    def display_setup(self):
        self.bus = smbus.SMBus(2) 
        self.address = 0x70
        self.bus.write_byte_data(self.address, 0x21, 0)   # Start oscillator (p10)
        self.bus.write_byte_data(self.address, 0x81, 0)   # Disp on, blink off (p11)
        self.bus.write_byte_data(self.address, 0xe7, 0)   # Full brightness (page 15)
        self.arr_setup()

    def arr_setup(self):
        self.out = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    def clear(self):
        self.out =  [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.baseTemp = self.get_temp() #reset baseline temp
        self.draw() #clear screen

    def move(self, dir):
        if dir == 'UP':
            if(self.cursor[1] % 8 != 7): #just checks if it is at upper limit
                self.cursor[1]+=1
                self.write_cursor()
        elif dir == 'DOWN':
            if(self.cursor[1] % 8 != 0):  #checks if it is at bottom limit
                self.cursor[1]-=1
                self.write_cursor()
        elif dir == 'LEFT':
            if(self.cursor[0] % 8 != 0): 
                self.cursor[0]-=1
                self.write_cursor()
        elif dir == 'RIGHT':
            if(self.cursor[0] % 8 != 7): 
                self.cursor[0]+=1
                self.write_cursor()
        self.draw()

    
    def write_cursor(self):
        self.out[(2*self.cursor[0])+self.color] |= 1 << self.cursor[1] #logic for setting color

    def draw(self):
        self.bus.write_i2c_block_data(self.address,0,self.out)

@app.route("/")
def index():
    templateData = {
        'title' : 'Etch-a-sketch',
        'color' : board.color
        }
    return render_template('EtchIndex.html', **templateData)

@app.route("/<task>")
def task(task):
    templateData = {
        'title' : 'Etch-a-sketch',
        'color' : board.color
        }

    if task == "clear":
        board.clear()
    elif task == "up":
        board.move('UP')
    elif task == "down":
        board.move('DOWN')
    elif task == "left":
        board.move('LEFT')
    elif task == "right":
        board.move('RIGHT')
    elif task == "toggle color":
        board.toggle_color()
    board.draw()
    return render_template('EtchIndex.html', **templateData)

if __name__ == "__main__":
    board = Board()
    app.run(host='0.0.0.0', port=8081, debug=True)


