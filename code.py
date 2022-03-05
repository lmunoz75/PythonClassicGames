# Escribe tu código aquí :-)
import time
import analogio
import board
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

x_axis = analogio.AnalogIn(board.A0)
y_axis = analogio.AnalogIn(board.A1)

def get_voltage(pin):
    return (pin.value * 3.3) / 65535    # ADC 12-bits [0 - 3.3]

while True:
    x = get_voltage(x_axis)
    y = get_voltage(y_axis)
    #print(f"x={x:.4f} | y={y:.4f}")

    if x < 0.3:
        keyboard.press(Keycode.LEFT_ARROW)
        time.sleep(0.1)
        keyboard.release(Keycode.LEFT_ARROW)

    elif x > 3.0:
        keyboard.press(Keycode.RIGHT_ARROW)
        time.sleep(0.1)
        keyboard.release(Keycode.RIGHT_ARROW)

    elif y < 0.3:
        keyboard.press(Keycode.DOWN_ARROW)
        time.sleep(0.1)
        keyboard.release(Keycode.DOWN_ARROW)

    elif y > 3.0:
        keyboard.press(Keycode.UP_ARROW)
        time.sleep(0.1)
        keyboard.release(Keycode.UP_ARROW)

    time.sleep(0.1)


