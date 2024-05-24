# https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf

from micropython import const
from usb.device.hid import HIDInterface

_INTERFACE_PROTOCOL_UNDEFINED = const(0x00)

class JoystickInterface(HIDInterface):
    def __init__(self):
        super().__init__(
            _JOYSTICK_REPORT_DESC,
            set_report_buf=bytearray(1),
            protocol=_INTERFACE_PROTOCOL_UNDEFINED,
            interface_str="Trill bar X-axis slider",
        )

    def send_joystick(self, x):
        value = x & 0xFF # converts signed to unsigned, 
        print(f"Sending joystick value: {value}")
        self.send_report(bytes([value]))

_JOYSTICK_REPORT_DESC = (
    b'\x05\x01'  # Usage Page (Generic Desktop)
        b'\x09\x04'  # Usage (Joystick)
    b'\xA1\x01'  # Collection (Application)
        b'\x09\x01'  # Usage (Pointer)
        b'\xA1\x00'  # Collection (Physical)
            b'\x09\x30'  # Usage (X) - X axis
            # b'\x09\x31'  # Usage (Y) - Y not used, here for visibility
            # b'\x09\x32'  # Usage (Z) - Z not used, here for visibility
            # b'\x09\x38'  # Steering not used, here for visibility
            b'\x15\x81'  # Logical Minimum (-127)
            b'\x25\x7F'  # Logical Maximum (127)
            b'\x75\x08'  # Report Size (8)
            b'\x95\x01'  # Report Count (1)
            b'\x81\x02'  # Input (Data, Variable, Absolute)
        b'\xC0'  # End Collection
    b'\xC0'  # End Collection
)