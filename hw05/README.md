# Homework 5

## Make
Running uname -a provides me this kernel version. Went from 5.10.168-ti-r75 to 5.10.168-ti-r74 \
![image](https://github.com/Navelwriter/ECE434-leeni/assets/77686570/95e045ef-0329-43b4-8e8f-c851e36e0c22)
## Kernel Source
## Kernel Modules 
### gpio_test
Found under the folder gpio_test, this one file completes both requirements of the assignment.
Given button input from both edges of P9_15, this toggles LED at P9_16 accordingly. \
This takes input from two more buttons, P8_15 and P8_18 to toggle the LEDs at P9_12 and P9_14. \
To run: \
First compile using `make` \
Load the kernel module by `sudo insmod gpio_test.ko` \
After running, remove the module by `sudo rmmod gpio_test`
## ADXL345 Accelerometer
After a new device is added, a folder in /sys/class/i2c-adapter/i2c-2/2-0053/iio:device0 is added. \
within this folder, you can access the following.
sampling freq, scale, calibration bias in x and y axis, x and y raw values, the name, and sampling_frequency.
### Etch-a-Sketch 
Located in /ADXL345 folder, this controls the etch_a_sketch app to be run using the ADXL345 accelerometer. 
To run setup script: initialize the accelerometer by running `sudo ./setup_adx1345` \
To run app: run using `python3 ./accel_temp.py` \
Best played when starting on a flat_surface, lift on each side to move the led_matrix led's accordingly.

## Kernel Module LED
Located in the /led folder, this ports the kernel_module LED example to have two different led timings \
Compile using 'make' \
Add the kernel module to the kernel using `sudo insmod led.ko` \
After use, remove the module by `sudo rmmod led`
