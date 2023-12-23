# import RPi.GPIO as GPIO

from connective import Connective, ConnectiveIO
from gpio_controller import GPIOController


class PiGPIOController(GPIOController):
    def __init__(self):
        super().__init__()
    
    def init(self):
        print('GPIO.setmode(GPIO.BCM)')
    
    def setup(self, pin, mode):
        print('GPIO.setup({}, GPIO.{})'.format(pin, 'IN' if mode == GPIOController.IN else 'OUT'))
    
    def cleanup(self):
        print('GPIO.cleanup()')
    
    def set(self, pin, value):
        print('GPIO.output({}, GPIO.{})'.format(pin, 'HIGH' if value == GPIOController.HIGH else 'LOW'))
    
    def get(self, pin):
        print('GPIO.input({})'.format(pin))


def main():
    connective = Connective(ConnectiveIO(
        clock = 'CLOCK',
        data = 'DATA',
        reset = 'RESET',
        stb_n = 'STB_N',
        addr = ['A0', 'A1', 'A2', 'A3']
    ), PiGPIOController())
    
    connective.matrix.select_chip_by_name('A1')
    connective.matrix.set_cross_xy(9, 3, 1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

