# Joyslide

This project demonstrates how to create a touch-sensitive steering wheel using the Trill Bar sensor and the Arduino Joystick library. The steering input is read from the Trill sensor and mapped to the steering axis of a virtual joystick, allowing you to control steering in a game or application by touching different positions on the Trill Bar.

## Hardware Requirements

- Arduino-compatible microcontroller
- Trill Bar sensor
- USB cable for programming and power

## Software Requirements

- [Arduino IDE](https://www.arduino.cc/en/software)
- [Arduino Joystick Library](https://github.com/MHeironimus/ArduinoJoystickLibrary)
- [Trill Arduino Library](https://github.com/BelaPlatform/Trill-Arduino)

## Installation

### Arduino Joystick Library

1. Download the latest version of the Joystick library from [this link](https://github.com/MHeironimus/ArduinoJoystickLibrary/archive/master.zip).
2. Open the Arduino IDE.
3. Go to `Sketch` > `Include Library` > `Add .ZIP Library...`.
4. Select the downloaded ZIP file and click `Open`. The Joystick library's examples will now appear under `File` > `Examples` > `Joystick`.

### Trill Arduino Library

1. Open the Arduino IDE.
2. Go to `Sketch` > `Include Library` > `Manage Libraries...`.
3. Search for "Trill" and install the Trill library by BelaPlatform.

Alternatively, you can download the library from [this link](https://github.com/BelaPlatform/Trill-Arduino) and install it using the same steps as for the Joystick library.

## Hardware Example

### Example Setup

- **Microcontroller**: SparkFun Qwiic Pro Micro - USB-C (ATmega32U4)
- **Connection Cable**: SparkFun Qwiic Cable - 50mm
- **Sensor**: Trill Bar
- **Power and Programming**: USB-C cable

### Optional Housing

For a neat setup, you can 3D print a housing for the Trill Bar using this [Trill_Bar_Stand.stl](https://www.thingiverse.com/thing:5320767) from Thingiverse.

### Connection Instructions

1. Connect the Trill Bar to the SparkFun Qwiic Pro Micro using the SparkFun Qwiic Cable.
2. Connect the SparkFun Qwiic Pro Micro to your computer using a USB-C cable.

### Special Note for Using the Qwiic Pro Micro

When setting up the SparkFun Qwiic Pro Micro in the Arduino IDE, follow these steps carefully to avoid common pitfalls:

- **Board Selection**: In the Arduino IDE, go to `Tools` > `Board` and select `SparkFun Pro Micro`.
- **Processor Selection**: Go to `Tools` > `Processor` and select `ATmega32U4 (5V, 16 MHz)`.

## Usage

1. Connect the Trill Bar sensor to your Arduino according to the Trill documentation.
2. Open the Arduino IDE and create a new sketch.
3. Copy and paste the provided code into the sketch.
4. Compile and upload the sketch to your Arduino.
5. (Optionally) open a serial monitor to observe the debug messages.
6. The joystick should now respond to touches on the Trill Bar.