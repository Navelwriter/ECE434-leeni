#!/usr/bin/python3

#Setup pygame
#import sys, pygame
#pygame.init()
#pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

#Setup the Matrix
import smbus
bus = smbus.SMBus(2)
matrix = 0x70
indexHold = [0x80, 0x00, 0x00, 0x00,
	 0x00, 0x00, 0x00, 0x00,
	 0x00, 0x00, 0x00, 0x00,
	 0x00, 0x00, 0x00, 0x00]

bus.write_byte_data(matrix, 0x21, 0)
bus.write_byte_data(matrix, 0x81, 0)
bus.write_byte_data(matrix, 0xe7, 0)

#Setup Flask
from flask import Flask, render_template, request
app = Flask(__name__)

#Print instructions
print("Etch-A-Sketch")
print("Move with website")

#Prompt for row and column numbers
rows = 8
columns = 8

#Initialize width and height to be about 500
#Should be exactly divisible by the numer of rows or columns 
size = width, height = int(500/columns)*columns, int(500/rows)*rows

#Set cursor
cursorleft = 0
cursortop = 0

#Track the row and column of the cursor
cursorCol = 0
cursorRow = 0

#Function to move the cursor up
def moveup():
	global cursortop,currRow,indexHold,cursorRow,cursorCol,matrix
	#If moving will put it outside of the screen, don't do it
	if (cursortop - height/rows) >= 0:
		#Move the cursor
		cursortop = cursortop - height/rows
		cursorRow = cursorRow - 1
		#Add the cursor position to the column array
		indexHold[(7-cursorCol) * 2] = indexHold[(7-cursorCol) * 2] | (0x01 << cursorRow)
		#Draw the blocks on the matrix
		bus.write_i2c_block_data(matrix, 0, indexHold)


#Function to move the cursor down
def movedown():
	global cursortop,currRow,indexHold,cursorRow,cursorCol,matrix
	#If moving will put it outside of the screen, don't do it
	if (cursortop + 2 * height/rows) <= width:
		#Move the cursor
		cursortop = cursortop + height/rows
		cursorRow = cursorRow + 1
		#Add the cursor position to the column array
		indexHold[(7-cursorCol) * 2] = indexHold[(7-cursorCol) * 2] | (0x01 << cursorRow)
		#Draw the blocks on the matrix
		bus.write_i2c_block_data(matrix, 0, indexHold)


#Function to move the cursor right
def moveright():
	global cursorleft,currColumn,indexHold,cursorCol,cursorRow,matrix
	#If moving will put it outside of the screen, don't do it
	if (cursorleft + 2 * width/columns) <= width:
		#Move the cursor
		cursorleft = cursorleft + width/columns
		cursorCol = cursorCol + 1
		#Add the cursor position to the column array
		indexHold[(7-cursorCol) * 2] = indexHold[(7-cursorCol) * 2] | (0x01 << cursorRow)
		#Draw the blocks on the matrix
		bus.write_i2c_block_data(matrix, 0, indexHold)


#Function to move the cursor left
def moveleft():
	global cursorleft,currColumn,indexHold,cursorCol,cursorRow,matrix
	#If moving will put it outside of the screen, don't do it
	if (cursorleft - width/columns) >= 0:
		#Move the cursor
		cursorleft = cursorleft - width/columns
		cursorCol = cursorCol - 1
		#Add the cursor position to the column array
		indexHold[(7-cursorCol) * 2] = indexHold[(7-cursorCol) * 2] | (0x01 << cursorRow)
		#Draw the blocks on the matrix
		bus.write_i2c_block_data(matrix, 0, indexHold)


#Function to clear the screen
def clear():
	global indexHold,cursorCol,cursorRow,matrix
#	screen.fill(white)
	for i in range (16):
		indexHold[i] = 0
	#Add the cursor position to the column array
	indexHold[(7-cursorCol) * 2] = indexHold[(7-cursorCol) * 2] | (0x01 << cursorRow)
	#Draw the blocks on the matrix
	bus.write_i2c_block_data(matrix, 0, indexHold)

#Clear the LED Matrix
clear()

#Basic case of the route for Flask
@app.route("/")
def index():
	template_data = {
		'title' : "Etch-A-Sketch Controls",
	}
	return render_template("etchASketchTemplate.html", **template_data)

#Route for flask based on the button press
@app.route("/<action>")
def action(action):
	#Select the action
	if action == 'right':
		moveright()
	elif action == 'left':
		moveleft()
	elif action == 'up':
		moveup()
	elif action == 'down':
		movedown()
	elif action == 'clear':
		clear()

	template_data = {
		'title' : "Etch-A-Sketch Controls",
	}

	return render_template("etchASketchTemplate.html", **template_data)

if __name__=="__main__":
	app.run(host='0.0.0.0', port=8081, debug=True)



