# Homework 4
## Memory Map
## mmap setup
| Purpose      | GPIO PIN | GPIO1 OFFSET|
| ----------- | ----------| --- |
| Button0     | P9_11     | 1<<30 |
| Button1     | P9_13     | 1<<31 |
## Kernel Driver
## Flask + Etch-a-Sketch
## LCD Display
The LCD is connected through SPI1
### Boris Photo
### mplayer Playback
To play gif format looping 5 times \
run ` mplayer -loop 5 -vo fbdev2:/dev/fb0 -vf scale=320:240 -framedrop girl.gif `

To play gif rotated 90 degrees (without looping)
run ' mplayer -vo fbdev2:/dev/fb0 -vf rotate=1 -vf-add scale=320:240 -framedrop girl.gif `

###
