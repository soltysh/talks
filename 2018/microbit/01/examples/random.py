from microbit import *
from random import randint

while True:
    if accelerometer.current_gesture() == "shake":
        display.show(str(randint(1, 6)))
