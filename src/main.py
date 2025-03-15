from machine import I2C, Pin
import time

# Define I2C addresses
RTC_DS_ADDR = 0x68
RTC_PCF_ADDR = 0x51


class WatchyRTC:
    def __init__(self, scl=22, sda=21):
        self.i2c = I2C(0, scl=Pin(scl), sda=Pin(sda))
        self.rtc_type = None
        self.init()

    def init(self):
        devices = self.i2c.scan()
        if RTC_DS_ADDR in devices:
            self.rtc_type = "DS3231"
        elif RTC_PCF_ADDR in devices:
            self.rtc_type = "PCF8563"
        else:
            raise Exception("No RTC module detected")

    def set_time(self, year, month, day, hour, minute, second):
        if self.rtc_type == "DS3231":
            self.i2c.writeto(
                RTC_DS_ADDR,
                bytes([0x00, second, minute, hour, 0, day, month, year - 2000]),
            )
        elif self.rtc_type == "PCF8563":
            self.i2c.writeto(
                RTC_PCF_ADDR,
                bytes([0x02, second, minute, hour, day, 0, month, year - 2000]),
            )
        else:
            raise Exception("RTC not initialized")

    def get_time(self):
        if self.rtc_type == "DS3231":
            self.i2c.writeto(RTC_DS_ADDR, bytes([0x00]))
            data = self.i2c.readfrom(RTC_DS_ADDR, 7)
        elif self.rtc_type == "PCF8563":
            self.i2c.writeto(RTC_PCF_ADDR, bytes([0x02]))
            data = self.i2c.readfrom(RTC_PCF_ADDR, 7)
        else:
            raise Exception("RTC not initialized")

        second, minute, hour, _, day, month, year = data
        return (year + 2000, month, day, hour, minute, second)


# Example usage
rtc = WatchyRTC()
print("Detected RTC:", rtc.rtc_type)
year, month, day, hour, minute, second = rtc.get_time()
print(f"Current time: {year}-{month}-{day} {hour}:{minute}:{second}")
