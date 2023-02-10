from time import sleep

from machine import Pin, PWM

DEFAULT_FAN_SPEED: int = 100
"""The perctange of duty cycle at which the fan should spin."""
FAN_MAX_DUTY_CYCLE: int = round(0.87 * 65535)
"""The maximum value for the duty cycle."""
DEFAULT_FAN_PIN: int = 27
"""The pin to which the fan is connected."""
FAN_FREQUENCY: int = 280000
"""The desired PWM frequency of the fan."""

DEFAULT_TOOL_PIN: int = 16
"""The pin to which the tool is connected."""

class Fan:
    """Manage the Fume Hood's Fan.

    Args:
        fan_pin: The PWM signal pin of tha fan
        fan_speed: The speed at which the fan should run (0-100) when the tool is removed

    """

    def __init__(self, fan_pin: int, fan_speed: int = DEFAULT_FAN_SPEED):
        self.pin = fan_pin
        self.fan_speed = fan_speed
        self.pwm = PWM(Pin(self.pin, Pin.OUT))
        self.pwm.freq(FAN_FREQUENCY)

        self.off()

    def set_speed(self, value: int):
        """Set the speed of the fan as an interger percent (0-100).

        Args:
            value: The speed for the fan.

        """
        if value == 0:
            value = FAN_MAX_DUTY_CYCLE
        else:
            value = round((1 - value / 100) * FAN_MAX_DUTY_CYCLE)
        self.pwm.duty_u16(value)

    def on(self):
        """Turn the fan on at the speed specified by ``self.fan_speed``"""
        self.set_speed(self.fan_speed)

    def off(self):
        """Turn off the fan."""
        self.set_speed(0)

class Tool:
    """Monitor te soldering iron on its dock.
    
    Args:
        tool_pin: The pin for the soldering iron
        fan: The fan to toggle via `Tool` presence

    """

    def __init__(self, tool_pin: int, fan: Fan):
        self.pin = tool_pin
        self.tool_active = False
        self.fan = fan
        self.tool = Pin(DEFAULT_TOOL_PIN, Pin.IN, Pin.PULL_DOWN)
        self.led = Pin('LED', Pin.IN)
        self.led.value(1)


    def remove_tool(self):
        """Remove the tool and turn on the fan."""
        if not self.tool_active:
            self.tool_active = True
            self.fan.on()

    def replace_tool(self):
        """Tool has been replaced, turn off the fan."""
        if self.tool_active:
            self.fan.off()
            self.tool_active = False

    def monitor(self):
        """Monitor the tool pin and dispatch based on tool presence."""
        while True:
            if self.tool.value():
                self.remove_tool()
            else:
                self.replace_tool()
            sleep(0.5)

if __name__ == '__main__':
    fan = Fan(DEFAULT_FAN_PIN, DEFAULT_FAN_SPEED)
    tool = Tool(DEFAULT_TOOL_PIN, fan)
    tool.monitor()
