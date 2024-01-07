#!/bin/bash
#only works in root rn

#initialize devices
cd /sys/class/i2c-adapter/i2c-2
#hard-coded for TMP101 in specific pins
if [ ! -e 2-0049 ]; then
    echo tmp101 0x49 > new_device
else
    echo "Could not find tmp101 in 0x49"
fi
if [ ! -e 2-004a ]; then
    echo tmp101 0x4a > new_device
else
    echo "Could not find tmp101 in 0x4a"
fi

cd 2-0049/hwmon/hwmon0
tmp1=`cat temp1_input`
cd ../../..
cd 2-004a/hwmon/hwmon1
tmp2=`cat temp1_input`
printf "tmp101_1 = %d mC \n tmp101_2 = %d mC \n" $tmp1 $tmp2
