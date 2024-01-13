import gpiod
from gpiod.line import Direction, Value

class GPIOPin():
    def __init__(self, gpiochip, consumer_name, pin):
        self.pin = pin
        self.request = gpiod.request_lines(
            gpiochip,
            consumer=consumer_name,
            config={
                pin: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)
            },
        )

    def set_active(self, flag):
        self.request.set_value(self.pin, Value.ACTIVE if flag else Value.INACTIVE)
