from machine import I2C, Pin, Timer
from trill import Bar
from touch import Touches1D
from time import sleep_ms, ticks_ms
import usb.device
import joystick

SCL_PIN = 9
SDA_PIN = 8
HAPTIC_PIN = 26

SENSOR_MIN = 0
SENSOR_MAX = 3200
SENSOR_CENTER = (SENSOR_MAX + SENSOR_MIN) // 2

JOYSTICK_MIN = -127
JOYSTICK_MAX = 127
JOYSTICK_CENTER = (JOYSTICK_MAX + JOYSTICK_MIN) // 2

POLL_FREQUENCY = 4  # (250hz)

THRESHOLD_PERCENTAGE = 0.15
DEADZONE_PERCENTAGE = 0.02
MOVEMENT_THRESHOLD_PERCENTAGE = 0.05

THRESHOLD = int(SENSOR_MAX * THRESHOLD_PERCENTAGE)
DEADZONE_START = int(SENSOR_MAX * (0.5 - DEADZONE_PERCENTAGE / 2))
DEADZONE_END = int(SENSOR_MAX * (0.5 + DEADZONE_PERCENTAGE / 2))
MOVEMENT_THRESHOLD = int(SENSOR_MAX * MOVEMENT_THRESHOLD_PERCENTAGE)

MAX_TOUCHES = 5

BAR = None
JOYSTICK = None
PULSE_SENT = False

# Initialize pin 26 as an output pin
haptic_pin = Pin(HAPTIC_PIN, Pin.OUT)


def init():
    global BAR, JOYSTICK

    try:
        i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
        print(f"I2C initialized: {i2c}")

        devices = i2c.scan()
        if devices:
            print("I2C devices found:", [hex(device) for device in devices])
        else:
            print("No I2C devices found")
            raise Exception("No I2C devices found")

    except OSError as e:
        print(f"I2C initialization error: {e}")
        raise

    try:
        BAR = Bar(i2c)
        print("Bar sensor initialized")
    except Exception as e:
        print(f"Error initializing Bar sensor: {e}")
        raise

    try:
        JOYSTICK = joystick.JoystickInterface()
        usb.device.get().init(JOYSTICK, builtin_driver=True)
        print("Joystick initialized")
    except Exception as e:
        print(f"Error initializing joystick: {e}")
        raise

    print("Waiting for joystick interface to open...")
    sleep_ms(100)


def turn_off_pin(timer):
    haptic_pin.value(0)  # Set the pin to low (turn the motor off)
    print("Pin turned off")


def loop():
    global JOYSTICK, PULSE_SENT

    try:
        touches = [{'location': -1, 'timestamp': 0, 'active': False} for _ in range(MAX_TOUCHES)]
        data = BAR.read()
        touches_data = Touches1D(data)

        num_touches = len(touches_data.get_touches())
        current_time = ticks_ms()

        matched_touches = [False] * MAX_TOUCHES

        for i in range(num_touches):
            current_location = touches_data.get_touches()[i][0]
            matched = False

            for j in range(MAX_TOUCHES):
                if touches[j]['active'] and abs(touches[j]['location'] - current_location) <= MOVEMENT_THRESHOLD:
                    touches[j]['location'] = current_location
                    matched_touches[j] = True
                    matched = True
                    break

            if not matched:
                for j in range(MAX_TOUCHES):
                    if not touches[j]['active']:
                        touches[j]['location'] = current_location
                        touches[j]['timestamp'] = current_time
                        touches[j]['active'] = True
                        matched_touches[j] = True
                        break

        for i in range(MAX_TOUCHES):
            if not matched_touches[i]:
                touches[i]['active'] = False

        latest_touch_index = -1
        latest_timestamp = 0
        for i in range(MAX_TOUCHES):
            if touches[i]['active'] and touches[i]['timestamp'] > latest_timestamp:
                latest_touch_index = i
                latest_timestamp = touches[i]['timestamp']

        steering_value = SENSOR_CENTER
        if latest_touch_index != -1:
            touch_location = touches[latest_touch_index]['location']

            if touch_location <= THRESHOLD:
                steering_value = SENSOR_MIN
                PULSE_SENT = False
            elif touch_location >= (SENSOR_MAX - THRESHOLD):
                steering_value = SENSOR_MAX
                PULSE_SENT = False
            elif touch_location >= DEADZONE_START and touch_location <= DEADZONE_END:
                steering_value = SENSOR_CENTER
                if not PULSE_SENT:
                    print("Steering center - activating pin")

                    # Turn on the pin (start the motor)
                    haptic_pin.value(1)
                    print("Pin turned on")

                    # Create a timer object
                    timer = Timer(-1)

                    # Set up the timer to call the turn_off_pin function after 150 milliseconds
                    timer.init(period=150, mode=Timer.ONE_SHOT, callback=turn_off_pin)

                    PULSE_SENT = True
            elif touch_location < DEADZONE_START:
                steering_value = map_value(touch_location, THRESHOLD, DEADZONE_START, SENSOR_MIN, SENSOR_CENTER)
                PULSE_SENT = False
            else:
                steering_value = map_value(touch_location, DEADZONE_END, SENSOR_MAX - THRESHOLD, SENSOR_CENTER, SENSOR_MAX)
                PULSE_SENT = False

        joystick_value = map_value(steering_value, SENSOR_MIN, SENSOR_MAX, JOYSTICK_MIN, JOYSTICK_MAX)
        print(f"Steering value: {steering_value}, Joystick value: {joystick_value}")
        JOYSTICK.send_joystick(joystick_value)

        sleep_ms(POLL_FREQUENCY)

    except OSError as e:
        print(f"Error reading from Bar sensor: {e}")


def map_value(value_to_map, input_min, input_max, output_min, output_max):
    mapped_value = (value_to_map - input_min) * (output_max - output_min) // (input_max - input_min) + output_min
    return mapped_value


if __name__ == '__main__':
    try:
        init()
        while True:
            loop()
    except Exception as e:
        print(f"Exception: {e}")
