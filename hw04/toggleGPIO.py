#
:/usr/bin/python3
from mmap import mmap
import time, struct

# Port Addresses
GPIO1_offset = 0x4804c000
GPIO1_size = 0x4804cfff-GPIO1_offset

GPIO_OE = 0x134
GPIO_SETDATAOUT = 0x194
GPIO_CLEARDATAOUT = 0x190
GPIO_DATAIN = 0x138

gpioToggle = 1<<12

# Next we need to make the mmap, using the desired size and offset:
with open("/dev/mem", "r+b" ) as f:
  mem1 = mmap(f.fileno(), GPIO1_size, offset=GPIO1_offset)

packed_reg = mem1[GPIO_OE:GPIO_OE+4]

reg_status = struct.unpack("<L", packed_reg)[0]

reg_status &= ~(gpioToggle)

mem1[GPIO_OE:GPIO_OE+4] = struct.pack("<L",reg_status)

try:
  while(True):
      #Toggle gpioToggle without delay
      mem1[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", gpioToggle)
      mem1[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L",gpioToggle)

except KeyboardInterrupt:
  mem1.close()
