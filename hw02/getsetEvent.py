#!/usr/bin/env python3
# //////////////////////////////////////
# 	getsetEvent.py
#   Like getset.py but uses events.
#   Get the value of P8_11 P8_12 P8_15 P8_16 and write it to P9_12 P9_14 P9_15 P9_16. 
# 	Wiring:	Attach a switch to P8_11 P8_12 P8_15 P8_16 and 3.3V and an LED to P9_12 P9_14 P9_15 P9_16.
# 	Setup:	sudo apt uupdate; sudo apt install libgpiod-dev
#           Run: gpioinfo | grep -i -e chip -e P9_14 to find chip and line numbers
# 	See:	https://github.com/starnight/libgpiod-example/blob/master/libgpiod-led/main.c
# //////////////////////////////////////
# Based on https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/tree/bindings/python/examples

import gpiod
import sys

CONSUMER='getset'
CHIP='1'
getoffsets=[13, 12, 15, 14] # P8_11 P8_12 P8_15 P8_16
setoffests=[28, 18, 16, 19] # P9_12 P9_14 P9_15 P9_16

def print_event(event):
    if event.type == gpiod.LineEvent.RISING_EDGE:
        evstr = ' RISING EDGE'
    elif event.type == gpiod.LineEvent.FALLING_EDGE:
        evstr = 'FALLING EDGE'
    else:
        raise TypeError('Invalid event type')

    print('event: {} offset: {} timestamp: [{}.{}]'.format(evstr,
                                                           event.source.offset(),
                                                           event.sec, event.nsec))

chip = gpiod.Chip(CHIP)

getlines = chip.get_lines(getoffsets)
getlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_BOTH_EDGES)

setlines = chip.get_lines(setoffests)
setlines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_DIR_OUT)

print("Hit ^C to stop")

while True:
    ev_lines = getlines.event_wait(sec=1)
    if ev_lines:
        for line in ev_lines:
            event = line.event_read()
            print_event(event)
    vals = getlines.get_values()

    #for val in vals:
    #	print(val, end=' ')
    #print('\r', end='')

    setlines.set_values(vals)
