# Homework 4
## Memory Map
| Memory Address| Description| Size|
| ----------- | ----------| --|
| 0xFFFF_FFFF     |      | |
| 0xBFFF_FFFF -> 0x8000_0000     | EMIF0_SDRAM     | 1GB|
| 0x481A_FFFF -> 0x481A_E000    |   GPIO3        | 8KB Total|
| 0x481A_DFFF -> 0x481A_C000    |   GPIO2        | 8KB Total|
| 0x481A_E000 -> 0x4804_C000    |   GPIO1        | 8KB Total|
| 0x44E0_8FFF -> 0x44E0_7000    |   GPIO0        | 8KB Total|
| 0x1FFF_FFFF -> 0x0000_0000 |  GPMC External Memory         |512MB|

## mmap setup
| Purpose      | GPIO PIN | GPIO1 OFFSET|
| ----------- | ----------| --- |
| Button0     | P9_11     | 1<<30 |
| Button1     | P9_13     | 1<<31 |

Both mmap files (buttonToggle.py and toggleGPIO.py) require a chmod +x as well as sudo permission to run
## mmap gpio toggle
I tried toggling the gpio without any sleep functions on oscilliscope to see what would happen \
I got the result of 140.9kHZ frequency. Compared to the maximum speed of 2.724kHZ for the .c gpiod toggling, mmap is much much faster.
![scope_2](https://github.com/Navelwriter/ECE434-leeni/assets/77686570/0da83ac7-6f82-401b-bdbd-8cf8fbdfaf8c)

## mmap led
This program simply toggles on and off the USR2 and USR3 built-in LEDS using button0 and button1.
You may need to disable USR2 and USR3 from its status led utilities to get this to work properly.

## Kernel Driver
This is run using ` ./kernelTMP101.sh ` \
This outputs the temperatures of the two I2C devices using the kernel hardware monitor (hwmon)
## Flask + Etch-a-Sketch
This maintains the use of the tmp101 sensors for clear and toggling color, but even these functionalities are also done using the web interface. \

After running 
` chmod +x etch_flask.py ` in hw04/etch \
This program is simply run using ` ./etch_flask.py` and going to http://192.168.7.2:8081/ \
![image](https://github.com/Navelwriter/ECE434-leeni/assets/77686570/00f1603a-c5c2-4015-811e-c4b6938e2496)

Credits go to Google Bard for making this look pretty after I got the basic functionality working.
![image](https://github.com/Navelwriter/ECE434-leeni/assets/77686570/3f06461d-4ae6-4e28-845e-3a333ae4717a)

## LCD Display
The LCD is connected through SPI1
### Boris Photo
To display the regular boris.png \
run ` sudo fbi -noverbose -T 1 -a boris.png ` \
<img src="./media/normalDog.jpg" width="500"> \
To rotate the image, I chose to modify the image instead of interfacing with fbi directly \
This was done using ` convert boris.png -rotate 90 borisRotate.png ` \
and displays with ` sudo fbi -noverbose -T 1 -a borisRotate.png ` \
<img src="./media/smartDog.jpg" width="500">

### mplayer Playback
To play gif format looping 5 times \


https://github.com/Navelwriter/ECE434-leeni/assets/77686570/cf67ba09-686c-456a-bb42-c3a6f238b041


run ` mplayer -loop 5 -vo fbdev2:/dev/fb0 -vf scale=320:240 -framedrop girl.gif `

To play gif rotated 90 degrees (without looping)


https://github.com/Navelwriter/ECE434-leeni/assets/77686570/8bfd5f7d-5d36-42a2-83e7-c4d8211cede3


run ' mplayer -vo fbdev2:/dev/fb0 -vf rotate=1 -vf-add scale=320:240 -framedrop girl.gif `
### Generate Text
Simply run ` ./text.sh `
<img src="./media/textDog.jpg" width="500">


###

# hw04 grading

| Points      | Description | |
| ----------- | ----------- | - |
|  2/2 | Memory map 
|  4/4 | mmap()
|  4/4 | i2c via Kernel
|  5/5 | Etch-a-Sketch via flask |  Nice use of Google Bard
|  5/5 | LCD display
|      | Extras
| 20/20 | **Total**

*My comments are in italics. --may*
