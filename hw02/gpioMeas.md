## GPIO Measurements

### blinkLED.sh (Questions are answered in table)
sleep time | min voltage (mv) | max voltage (mv)| period(ms) | frequency(Hz) | htop process(%) | stable? | stable w/ vi?|
| ----------- | ----------- |---|---|---|---|---|---|
| 0.5  | -8.21   |336 | 1025| 0.976 | 0.7 | yes| yes|
| 0.25  | -8.   |336 | 520| 1.87 | 0.7 | yes| yes|
| 0.1  | -8.21   |336 | 225| 4.4 | 1.9 | yes| yes|
| 0.05 | -8.21   |336 | 122.5| 8.13 | 4.0 | yes| yes|
| 0.02  | -8.21   |336 | 62.5| 16.0 | 7.2 | yes,somewhat| on start, varies|
| 0.01  | -8 (fluctuates)   |345 | 33| 20.4 | 15 | not really| not more than normal|
| 0.05  | -8 (fluctuates)   |345 | 43| 23.8 | 11.4 | periods fluctuate| no at start|
| 0.01  | -8 (fluctuates)   |345 | 46| 40 | 20 | no| no|
| none | -300 | 400|no|no |no |no |no |no |
What's the min and max voltage? (for sleep(0.5))
3.36V, -8mV
What period and frequency is it? (for sleep(0.5))
1025ms , 0.976
Fastest Period? 
46ms 
Try cleaning up blinkLED.sh
I didn't notice any difference when it came to consistency, I even tried removing sleep, which just made it a solid block of signals. 


### blinkLED.py
sleep time | period(ms) | frequency(Hz) | htop process(%) | stable? |
|---|---|---|---|---|
| 0.1  | 201| 4.98 | 0.7 | yes|
| 0.05  | 101| 9.9 | 3.3 | yes|
| 0.02  | 41.5| 24.1 | 2.0 | yes|
| 0.01  | 21| 48 | 4 | yes|
| 0.002  | 200| 192 |16 | yes|
| 0.001  | 3| 330 | 30 | yes|
| 0.0005  | 1.9| 500 | 52 | no|
| 0.00025  | 0.760| 1280 | 75 | no|

### blinkLED.c
I just found the fastest blink time just to save myself some time documenting. 
period(ms) | frequency(kHz) | htop process(%) | stable? |
|---|---|---|---|
|0.367|2.724|62%|somewhat|

### gpiod testing
filename | Shortest Period  | frequency | htop process(%) | 
|---|---|---|---|
|toggle1.py|210.1 us|4.76 KHz| 66.4 |
|toggle1.c| 180.0 us| 5.5 KHz| 62.0 |
|toggle2.py| 226.3 us| 4.424 KHz| 84.1 |
|toggle2.c| 166.6 us| 6.0 KHz| 55.2 |
