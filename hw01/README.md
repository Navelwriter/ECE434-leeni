Written by Noah Lee for ECE434
This is my implementation of "Etch-a-sketch" running on python in the Beaglebone Black

## How to run
in the directory of this repo, run 
```
python ./etch.py
```
## Simple Runthrough
This will first prompt you to input the dimensions of the canvas
This can only be a maximum of 80 in the x-axis and 30 in the y-axis
Once you are able to draw there are the following commands:
```
q #this quits the application
```
```
f #this allows you to input any character and changes the shape of the cursor to it
```
```
c #this clears the board
```
```
arrow keys #this moves the cursor
```

# hw01 grading

| Points      | Description | Comment
| ----------- | ----------- | -------
|  8/8 | Etch-a-Sketch works | 
|  2/2 | Code documented (including name) |
|  2/2 | Includes #!/usr/bin/env python3 and chmod +x |
|  2/2 | install.sh included if needed |
|  2/2 | Used hw01 directory |
|  2/2 | ReadMe.md included |
|  0/2 | Name in gitLearn and gitLearnFork | 
| 18/20 | **Total**