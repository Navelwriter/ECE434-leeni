#//////////////////////////////////////
# Noah Lee 
# ECE 434 hw01: Etch-a-sketch
# 12/10/2023
#//////////////////////////////////////

#!/usr/bin/env python3
#chmod +x etch.py

# import argparse
import smbus
import gpiod
import time

bus = smbus.SMBus(2)
leftTMP = 0x49
rightTMP = 0x4A

offset = 5
GREEN = 0
RED = 1
debounce = 0

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
        self.dial_setup()
    
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

    def dial_setup(self):
        left_dial = '/dev/bone/counter/2/count0/'
        right_dial = '/dev/bone/counter/1/count0/'
        maxCounter = "1000000"
        with open(f'{left_dial }/ceiling', 'w') as f:
            f.write(maxCounter)
        with open(f'{right_dial }/ceiling', 'w') as f:
            f.write(maxCounter)
        # enable both counters
        with open(f'{left_dial }/enable', 'w') as f:
            f.write('1')
        with open(f'{right_dial }/enable', 'w') as f:
            f.write('1')
        # open and store encoder positions
        self.left_data = open(f'{left_dial }/count', 'r')
        self.right_data = open(f'{right_dial }/count', 'r')
        self.get_dial_pos()

    def get_dial_pos(self):
        self.left_old = read_data(self.left_data)
        self.right_old = read_data(self.right_data)

    def get_data(self):
        left = read_data(self.left_data)
        right = read_data(self.right_data)
        if left > self.left_old + offset:
            self.left_old = left
            self.move('DOWN') 
        elif left < self.left_old - offset:
            self.left_old = left
            self.move('UP')      
        if right > self.right_old + offset:
            self.right_old = right
            self.move('RIGHT')
        elif right < self.right_old - offset:
            self.right_old = right
            self.move('LEFT')

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
    
    def write_cursor(self):
        self.out[(2*self.cursor[0])+self.color] |= 1 << self.cursor[1] #logic for setting color

    def draw(self):
        self.bus.write_i2c_block_data(self.address,0,self.out)

def read_data(file_name):
    file_name.seek(0)
    data = file_name.read()[:-1]
    return int(data)

def main():
    board = Board()
    try:
        while(True):
            board.get_data()
            board.draw()
            board.compare_temp()
            print(board.out,end="\r")
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\n Byebye \n")
        board.clear()
        return 1
main()
