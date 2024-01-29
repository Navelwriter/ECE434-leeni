## Homework 7: 1-wire 
## By: Noah Lee
### Introduction:
For this assignment we had two main components: \n
- Implementing the device tree and a program to read three MAX31820 1-wire temperature sensors on Pin P9_14.
- Write a systemd sercive that automatically starts my flask client on bootup


I decided to combine both of these assignments into a single flask server that will read the temperature sensors that launches on boot.
### Usage:
To add the flask server to systemd, update the flask.service to reflect your file system and move the flask.service to /lib/systemd/system/
To make it start on bootup, run `sudo systemctl enable flask` \
Either start the service with `sudo systemctl start flask` or on boot and point browser to 192.168.7.2:8081 \
You should see three temperatures and a button, press the button to refresh the temperature sensor data displayed
![image](https://github.com/Navelwriter/ECE434-leeni/assets/77686570/364859e2-99b5-44c1-887d-97e36dc99fe5)

End the service with `sudo systemctl stop flask`
