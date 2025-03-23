from lib.display import Display
from lib.watchy_rtc import WatchyRTC
from machine import Pin,  ADC, WDT, Timer
import esp32
import machine
import asyncio

from utils import (
    hour_to_string,
    number_teen_to_string,
    number_tens_to_string,
    month_to_short_string,
    week_day_to_short_string,
)
from lib.constants import (
    MENU_PIN,
    BACK_PIN,
    UP_PIN,
    DOWN_PIN,
    RTC_SDA_PIN,
    RTC_SCL_PIN,
    RTC_INT_PIN,
    BATT_ADC_PIN,
    WHITE,
    BLACK,
)

import assets.fonts.fira_sans_bold_58 as fira_sans_bold_58
import assets.fonts.fira_sans_regular_38 as fira_sans_regular_38
import assets.fonts.fira_sans_regular_28 as fira_sans_regular_28


DEBUG = False


class Watchy:
    def __init__(self):
        self.wdt = WDT(timeout=30000)
        self.wdt_timer = Timer(0)
        self.wdt_timer.init(mode=Timer.PERIODIC,
                            period=10000, callback=self.feed_wdt)

        self.display = Display()
        self.rtc = WatchyRTC()
        self.rtc.start_alarm()
        self.adc = ADC(Pin(BATT_ADC_PIN, Pin.IN))

        self.init_interrupts()
        self.init_buttons()
        self.handle_wakeup()
        if not DEBUG:
            machine.deepsleep()

    def init_interrupts(self):
        esp32.wake_on_ext0(Pin(RTC_INT_PIN, Pin.IN), esp32.WAKEUP_ALL_LOW)

        buttons = (
            Pin(MENU_PIN, Pin.IN),
            Pin(BACK_PIN, Pin.IN),
            Pin(UP_PIN, Pin.IN),
            Pin(DOWN_PIN, Pin.IN),
        )
        esp32.wake_on_ext1(buttons, esp32.WAKEUP_ANY_HIGH)
        # NOTE: it is not possible to get the wakeup bit in MicroPython yet
        # see https://github.com/micropython/micropython/issues/6981

    def init_buttons(self):
        menu_pin = Pin(26, Pin.IN)
        back_pin = Pin(25, Pin.IN)
        up_pin = Pin(32, Pin.IN)
        down_pin = Pin(4, Pin.IN)
        # for pin in [menu_pin]:  # back_pin, up_pin
        #    self.set_pin_handler(pin)

    def set_pin_handler(self, pin: Pin):
        pin.irq(
            handler=self.handle_pin_wakeup,
            trigger=Pin.WAKE_HIGH,
            wake=machine.DEEPSLEEP,
        )

    def handle_wakeup(self):
        reason = machine.wake_reason()
        if reason is machine.EXT0_WAKE or reason == 0:
            print("RTC wake")
            self.display_prose_watchface()
            self.rtc.clear_alarm()
        elif reason is machine.EXT1_WAKE:
            print("PIN wake")
            p = Pin(MENU_PIN, Pin.IN)
            print(p.value())
        else:
            print("Wake for other reason")
            print(reason)

    def handle_pin_wakeup(self, pin: Pin):
        print("handle_pin_wakeup")
        print(pin)

    def display_prose_watchface(self):
        self.display.framebuf.fill(WHITE)
        datetime = self.rtc.get_time()
        year, month, date, week_day, hours, minutes, seconds = datetime
        self.display.display_text(
            hour_to_string(hours), 10, 15, fira_sans_bold_58, WHITE, BLACK
        )

        def display_minutes_1(text): return self.display.display_text(
            text, 10, 80, fira_sans_regular_38, WHITE, BLACK
        )
        if minutes == 0:
            display_minutes_1("o'clock")
        elif minutes < 20:
            display_minutes_1(
                "oh " if minutes < 10 else "" + number_teen_to_string(minutes)
            )
        else:
            minutes_tens_str, minutes_ones_str = number_tens_to_string(minutes)
            display_minutes_1(minutes_tens_str)
            self.display.display_text(
                minutes_ones_str, 10, 115, fira_sans_regular_38, WHITE, BLACK
            )
        week_day_str = week_day_to_short_string(week_day)
        month_str = month_to_short_string(month)
        self.display.display_text(
            f"{week_day_str}, {date} {month_str}",
            10,
            160,
            fira_sans_regular_28,
            WHITE,
            BLACK,
        )
        self.display.update()

    def get_battery_voltage(self) -> float:
        return self.adc.read_uv() / 1000 * 2

    def feed_wdt(self, timer):
        # TODO: verify that everything is functioning correctly
        self.wdt.feed()
