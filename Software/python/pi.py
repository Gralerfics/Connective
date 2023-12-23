import RPi.GPIO as GPIO

from connective import Connective, ConnectiveIO
from gpio_controller import GPIOController


class PiGPIOController(GPIOController):
    def __init__(self):
        super().__init__()
    
    def init(self):
        GPIO.setmode(GPIO.BCM)
    
    def setup(self, pin, mode):
        GPIO.setup(pin, GPIO.IN if mode == GPIOController.IN else GPIO.OUT)
    
    def cleanup(self):
        GPIO.cleanup()
    
    def set(self, pin, value):
        GPIO.output(pin, GPIO.HIGH if value == GPIOController.HIGH else GPIO.LOW)
    
    def get(self, pin):
        return GPIOController.HIGH if GPIO.input(pin) else GPIOController.LOW


def main():
    connective = Connective(ConnectiveIO(
        clock = 0,
        data = 0,
        reset = 0,
        stb_n = 0,
        addr = [0, 0, 0, 0]
    ), PiGPIOController())
    
    # 0 - AC0
    connective.matrix.select_chip_by_name('A0')
    connective.matrix.set_cross_xy(8, 0, 1)
    
    # AC0 - 19
    connective.matrix.select_chip_by_name('C0')
    connective.matrix.set_cross_xy(0, 3, 1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

