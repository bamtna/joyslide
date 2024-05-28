# ??

This is a MicroPython port of [bamtna's joyslide project](https://github.com/bamtna/joyslide/tree/main) which utilizes a Trill Bar as a touch-sensitive input device that is mapped to the axis of a joystick.

## Hardware

- Microcontroller capable of running a machine.USBDevice compatible port of MicroPython (I used a Pi Pico w/rp2040 board)
- Trill Bar sensor
- Vibrating motor like [Adafruit 1201](https://www.adafruit.com/product/1201) if haptic feedback is desired
- USB Cable

## Software

- [MicroPython usb-device-hid hid.py library](https://github.com/micropython/micropython-lib/tree/master/micropython/usb/usb-device-hid)
- [MicroPython usb-device core.py library](https://github.com/micropython/micropython-lib/tree/master/micropython/usb/usb-device-hid)
- [mpremote](https://pypi.org/project/mpremote/) (pip install mpremote)

## Case
[Bela's Trill Bar case](https://www.thingiverse.com/thing:5320767) is available here.

Additionally, I've drawn several trim pieces that fit snugly over top to aid in tactile feedback.  All models are available [on Thingiverse here.](https://www.thingiverse.com/thing:6630614)

## Hardware Instructions

GPIO pins specific to Pi Pico, will change from board to board.
If you need to change pins, modify SCL_PIN and SDA_PIN variables in main.py

- Solder wire from GPIO 8 on Pi Pico to SCL pad on Trill Bar
- Solder wire from GPIO 9 on Pi Pico to SCL pad on Trill Bar
- Solder wire from 3v3 on Pi Pico to VCC pad on Trill Bar
- Solder wire from GND on Pi Pico to GND pad on Trill bar

If using haptic feedback motor:

- Solder positive lead to pin 26
- Solder negative lad to GND

A Qwiic cable can also be used for one or both connections if your board supports it.


## Software Installation

1.  Download MicroPython libraries listed in Software Requirements
2.  Install mpremote, ensure it's in PATH to pick up environment var
3.  Open a terminal
4.  Copy relevant main_*.py, joystick.py, and the USB libraries (making sure to preserve file structure)
    - `mpremote cp main_*.py :main.py`
    - `mpremote cp joystick.py :joystick.py`
    - `mpremote mkdir usb\device`
    - `mpremote cp usb.py :\usb\device\usb.py`
    - `mpremote cp hid.py :\usb\device\hid.py`
5.  Reset the board with `mpremote soft-reset`
6.  (optional) open up gamepad configuration to check if it all worked

Serial monitor can be used to view logging.

## Troubleshooting

If the device has issues, run trill_print_touch.py with a serial monitor to verify the sensor is working properly.