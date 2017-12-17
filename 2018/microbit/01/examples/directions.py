from microbit import *

dot = Image(
"00000:"
"00000:"
"00200:"
"00000:"
"00000"
)


while True:
    gesture = accelerometer.current_gesture()
    if gesture == "up":
        display.show(Image.ARROW_S)
    elif gesture == "down":
        display.show(Image.ARROW_N)
    elif gesture == "left":
        display.show(Image.ARROW_W)
    elif gesture == "right":
        display.show(Image.ARROW_E)
    else:
        display.show(dot)
