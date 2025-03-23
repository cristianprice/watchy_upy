import machine
import utime
from pcf8563 import PCF8563


# Initialize I2C (example for ESP32)
i2c = machine.I2C(1, scl=machine.Pin(22), sda=machine.Pin(21))

# Initialize the PCF8563 RTC
rtc = PCF8563(i2c)

# Set the alarm to trigger every minute
rtc.set_daily_alarm(minutes=0)  # 0x80 means every minute

# Enable the alarm interrupt
rtc.enable_alarm_interrupt()

# Define the pin for RTC interrupts
rtc_interrupt_pin = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)

# Function to handle the interrupt


def handle_rtc_interrupt(pin):
    if rtc.check_for_alarm_interrupt():
        print("Alarm interrupt triggered")
        # Clear the alarm interrupt
        rtc.clear_alarm()


# Attach the interrupt handler to the pin
rtc_interrupt_pin.irq(trigger=machine.Pin.IRQ_FALLING,
                      handler=handle_rtc_interrupt)
