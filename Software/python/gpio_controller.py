from enum import Enum


class GPIOController:
    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1
    
    def __init__(self):
        self.init()
    
    def init(self):
        pass
    
    def setup(self, pin, mode):
        pass
    
    def cleanup(self):
        pass

    def set(self, pin, value):
        pass

    def get(self, pin):
        pass

