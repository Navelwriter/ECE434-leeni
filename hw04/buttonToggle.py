#!/usr/bin/python3
from mmap import mmap
import time, struct

# Port Addresses
GPIO0_offset = 0x44e07000
GPIO0_size = 0x44e07fff-GPIO0_offset

GPIO1_offset = 0x4804c000
GPIO1_size = 0x4804cfff-GPIO1_offset

GPIO_OE = 0x134
GPIO_SETDATAOUT = 0x194
GPIO_CLEARDATAOUT = 0x190
GPIO_DATAIN = 0x138

USR3 = 1<<24
USR2 = 1<<23

butt1 = 1<<30 #P9_11
butt2 = 1<<31 #P9_13

butt1_debounce= 0
butt2_debounce = 0
butt1_status = 0
butt2_status = 0

# Next we need to make the mmap, using the desired size and offset:
with open("/dev/mem", "r+b" ) as f:
  mem0 = mmap(f.fileno(), GPIO0_size, offset=GPIO0_offset)
  mem1 = mmap(f.fileno(), GPIO1_size, offset=GPIO1_offset)

packed_reg = mem1[GPIO_OE:GPIO_OE+4]

reg_status = struct.unpack("<L", packed_reg)[0]

reg_status &= ~(USR2)
reg_status &= ~(USR3)

mem1[GPIO_OE:GPIO_OE+4] = struct.pack("<L",reg_status)

try:
  while(True):
    packed_in = mem0[GPIO_DATAIN:GPIO_DATAIN+4]
    gpio_in = struct.unpack("<L", packed_in)[0]
    time.sleep(0.05)
    #Toggle USR3 LED using Button1
    if (gpio_in & butt1)==0:
      if butt1_debounce == 0:
        if(butt1_status == 1):
          mem1[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", USR3)
          butt1_status = 0
        else:
          mem1[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", USR3)
          butt1_status = 1
        butt1_debounce = 1
    else:
      if(butt1_debounce == 1):
        butt1_debounce = 0
    #Toggle USR2 LED using Button2
    if (gpio_in & butt2)==0:
      if butt2_debounce == 0:
        if(butt2_status == 1):
          mem1[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", USR2)
          butt2_status = 0
        else:
          mem1[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", USR2)
          butt2_status = 1
        butt2_debounce = 1
    else:
      if(butt2_debounce == 1):
        butt2_debounce = 0





except KeyboardInterrupt:
  mem0.close()
  mem1.close()
