#!/usr/bin/python3
from mmap import mmap
import time, struct
import gpiod

# Port Addresses
GPIO1_offset = 0x4804c000
GPIO1_size = 0x4804cfff-GPIO1_offset
GPIO_OE = 0x134
GPIO_SETDATAOUT = 0x194
GPIO_CLEARDATAOUT = 0x190
greenLED = 1<<24
blueLED = 1<<23

CONSUMER='getset'
CHIP='1'
getoffsets=[13, 12]
LEDoffsets = [greenLED, blueLED]

chip = gpiod.Chip(CHIP)
lines = chip.get_lines(getoffsets)
lines.request(consumer=CONSUMER, type=gpiod.LINE_REQ_EV_RISING_EDGE)
last_val = lines.get_values()

butt1_status = 0
butt2_status = 0

# Next we need to make the mmap, using the desired size and offset:
with open("/dev/mem", "r+b" ) as f:
  mem = mmap(f.fileno(), GPIO1_size, offset=GPIO1_offset)

packed_reg = mem[GPIO_OE:GPIO_OE+4]

reg_status = struct.unpack("<L", packed_reg)[0]

reg_status &= ~(greenLED)
reg_status &= ~(blueLED)

mem[GPIO_OE:GPIO_OE+4] = struct.pack("<L",reg_status)

try:
  while(True):
      butt_in = lines.event_wait(sec=1)
      if(butt_in):
          butt = lines.get_values()
          print(butt)
          for k in range(len(butt)):
              if butt[k] != last_val[k]:
                  if butt[k]:
                      mem[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L",LEDoffsets[k])
                  else:
                      mem[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L",LEDoffsets[k])
                  last_val[k] = butt[k]



except KeyboardInterrupt:
  mem.close()
