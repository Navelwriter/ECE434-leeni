The oscilliscope testing and answers can be found in gpioMeas.md

The getsetEvent.py that interfaces with my buttons and leds are foundi n getsetEvent.py

| Purpose      | GPIO PIN | GPIO NO|
| ----------- | ----------| --- |
| Button0     | P8-11     | 13 |
| Button1     | P8-12     | 12 |
| Button2     | P8-15     | 15 |
| Button3     | P8-16     | 14 |
| LED0(Red)   | P9-12     | 28 |
| LED0(Yellow)| P9-14     | 18 |
| LED0(Green) | P9-15     | 16 |
| LED0(Blue)  | P9-16     | 19 |

This is my implementation of "Etch-a-sketch" running on python in the Beaglebone Black that uses push buttons as inputs

## How to run
in the directory of this repo, run 
```
python ./etch.py
```
## Simple Runthrough
This will first prompt you to input the dimensions of the canvas using keyboard
This can only be a maximum of 80 in the x-axis and 30 in the y-axis
Here are the following movement commands:
### Movement
| Button      | Function | 
| ----------- | ----------| 
| Button0     | UP     |
| Button1     | DOWN     |
| Button2     | LEFT     |
| Button3     | RIGHT     |
### Combination Keys
These are when you press two buttons at the same time to perform special functions
Please note that button presses are not properly debounced so the cursor may move when performing these operations
| Combo      | Function | 
| ----------- | ----------| 
| Button0 + Button1    | CLEAR SCREEN     |
| Button1 + Button2    | TOGGLE BETWEEN DRAW AND ERASE     |
| Button2 + Button3    | QUIT APPLICATION    |

