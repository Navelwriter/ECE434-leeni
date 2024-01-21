#!/bin/bash
#only works in root rn

#initialize devices
cd /sys/class/i2c-adapter/i2c-2
#hard-coded for ADX1345 in specific pins
if [ ! -e 2-0053 ]; then
    echo adxl345 0x53 > new_device
else
    echo "Could not find adxl345 in 0x53"
fi

echo "Finished setup"
