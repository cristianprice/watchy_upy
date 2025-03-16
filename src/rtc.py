from lib.pcf8563 import PCF8563
from machine import I2C, Pin

RTC_PCF_ADDR = 0x51


class WatchyRTC:
    def __init__(self, scl=22, sda=21):
        self.i2c = I2C(0, scl=Pin(scl), sda=Pin(sda))
        self.rtc = PCF8563(self.i2c, RTC_PCF_ADDR)

    async def get_time(self):
        '''
        Return a tuple such as (year, month, date, day, hours, minutes, seconds).
        '''
        return self.rtc.datetime()

    async def set_time(self, year, month, day, date, hour, minute, second):
        self.rtc.write_all(second, minute, hour, day, date, month, year)

    async def set_now(self):
        self.rtc.write_now()
