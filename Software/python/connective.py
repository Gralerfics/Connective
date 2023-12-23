import time

from gpio_controller import GPIOController


class ConnectiveIO:
    def __init__(self, clock, data, reset, stb_n, addr):
        self.clock = clock
        self.data = data
        self.reset = reset
        self.stb_n = stb_n
        self.addr = addr # list of 4 pins


class CH446QMatrix:
    def __init__(self, connective):
        self.connective = connective
    
    def nop(self):
        time.sleep(2e-5)
    
    def set_clock(self, value):
        self.connective.gpio.set(self.connective.io.clock, value)
    
    def set_reset(self, value):
        self.connective.gpio.set(self.connective.io.reset, value)
    
    def set_data(self, value):
        self.connective.gpio.set(self.connective.io.data, value)
    
    def set_stb(self, value):
        self.connective.gpio.set(self.connective.io.stb_n, self.connective.gpio.LOW if value == self.connective.gpio.HIGH else self.connective.gpio.HIGH)
    
    def select_chip(self, chip_addr):
        for i in range(4):
            self.connective.gpio.set(self.connective.io.addr[i], int(chip_addr & (1 << i) > 0))
    
    def select_chip_by_name(self, chip_name):
        # chip_name: 'A0', 'A1', 'B0', 'B1', 'C0', 'C1', 'D0', 'D1', 'E0', 'E1'
        chip_addr = (ord(chip_name[0]) - 65) << 1 | (ord(chip_name[1]) - 48)
        self.select_chip(chip_addr)
    
    def reset(self):
        self.set_reset(1)
        self.nop()
        self.set_reset(0)
        self.nop()
    
    def stb(self):
        self.set_stb(1)
        self.nop()
        self.set_stb(0)
        self.nop()
    
    def select_cross(self, x, y):
        addr = (y << 4) | x
        for i in range(6, -1, -1):
            self.set_data(int(addr & (1 << i) > 0))
            self.nop()
            self.set_clock(0)
            self.nop()
            self.set_clock(1)
            self.nop()
    
    def set_cross(self, value):
        self.set_stb(0)
        self.set_data(value)
        self.nop()
        self.set_stb(1)
        self.nop()
        self.set_stb(0)
        self.nop()
    
    def set_cross_xy(self, x, y, value):
        self.select_cross(x, y)
        self.set_cross(value)
    
    pass


class Connective:
    def __init__(self, io: ConnectiveIO, gpio_controller: GPIOController):
        self.io = io
        self.gpio = gpio_controller
        
        self.gpio.init()
        self.gpio.setup([self.io.clock, self.io.data, self.io.reset, self.io.stb_n, *self.io.addr], self.gpio.OUT)
        
        self.matrix = CH446QMatrix(self)
        self.matrix.set_clock(0)
        self.matrix.set_reset(0)
        self.matrix.set_stb(0)
        self.matrix.reset()

    # def 

