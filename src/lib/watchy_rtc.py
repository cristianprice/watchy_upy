from lib.pcf8563 import PCF8563
from machine import I2C, Pin
from lib.constants import RTC_PCF_ADDR, RTC_INT_PIN


class WatchyRTC:
    def __init__(self, scl=22, sda=21):
        self.i2c = I2C(0, scl=Pin(scl), sda=Pin(sda))
        self.rtc = PCF8563(self.i2c, RTC_PCF_ADDR)

    def get_time(self):
        '''
        Return a tuple such as (year, month, date, day, hours, minutes, seconds).
        '''
        return self.rtc.datetime()

    def set_time(self, year, month, day, date, hour, minute, second):
        self.rtc.write_all(second, minute, hour, day, date, month, year)

    def set_now(self):
        self.rtc.write_now()

    def start_alarm(self):
        # Set the alarm to trigger every minute
        self.rtc.set_daily_alarm(minutes=1)
        self.rtc.enable_alarm_interrupt()
