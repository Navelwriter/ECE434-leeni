## Pin Assignments 
|Name|Pin Assignment|GPIO num|
|---|---|---|
|Dial Left|P8-11,P8-12|45,44|
|Dial Right|P8-33,P8-35|9,8|
|I2C SCL|P9-19|I2C2|
|I2C SDL|P9-20|I2C2|

## I2C Assignments
|Name|Bus Number|Address|
|---|---|---|
|TMP101 (left)|2|0x49|
|TMP101 (right)|2|0x4a|
|Dot Matrix|2|0x70|

## Instructions:
### readTMP101.py
simply run \
`` python readTMP101.py ``

### etch_temp.py
#### Description
This program uses both TMP101 sensors, rotary encoders, and the I2C dot-matrix display to run the etch-a-sketch program \
#### Usage
To setup the rotary encoders as eqep run the script setup.sh with \
`` ./setup.sh `` \
Then run etch_temp.py with \
`` python etch_temp.py``\
### Features
Turn the left rotary dial clockwise to move the cursor UP and anti-clockwise to move it DOWN\
\
Turn the right rotary dial clockwise to move the cursor RIGHT and anti-clockwise to move it LEFT\
\
Increase the temperature of the left TMP101 to toggle the color between RED and GREEN (GREEN is default)\
\
Increase the temperature of the right TMP101 to clear the screen\
\
ctrl+c on host keyboard to quit the program

# hw03 grading

| Points      | Description | |
| ----------- | ----------- |-|
|  4/8 | TMP101 | Didn't use /sys/class/i2c-adapter/i2c-2/new_device 
|  2/2 |   | Documentation 
|  6/5 | Etch-a-Sketch | Nice use of TMP101 to clear screen
|  3/3 |   | setup.sh
|  2/2 |   | Documentation
| 17/20 | **Total**

*My comments are in italics. --may*
