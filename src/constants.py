from micropython import const

WHITE = const(1)
BLACK = const(0)

RTC_PCF_ADDR = const(0x51)

RTC_SDA_PIN = const(21)
RTC_SCL_PIN = const(22)

MENU_BTN_PIN = const(26)
BACK_BTN_PIN = const(25)
DOWN_BTN_PIN = const(4)
UP_BTN_PIN = const(35)

DISPLAY_CS = const(5)
DISPLAY_RES = const(9)
DISPLAY_DC = const(10)
DISPLAY_BUSY = const(19)
ACC_INT_1_PIN = const(14)
ACC_INT_2_PIN = const(12)
VIBRATE_MOTOR_PIN = const(13)
RTC_INT_PIN = const(27)

BATT_ADC_PIN = const(34)
