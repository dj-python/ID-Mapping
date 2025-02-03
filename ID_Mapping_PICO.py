from machine import Pin, I2C
import time
import W5500_EVB_PICO as W5500
import sys

class MainFW:
    def __init__(self):
        # I2C 0,1번 초기화
        self.i2c_0 = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
        self.i2c_1 = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)

        # I2C 버스에 연결된 장치 주소 스캔
        self.devices = self.i2c_0.scan()
        self.devices = self.i2c_1.scan()
