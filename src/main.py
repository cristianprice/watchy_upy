import machine
import esp32
import time
from constants import MENU_BTN_PIN, UP_BTN_PIN, DOWN_BTN_PIN, BACK_BTN_PIN
from utils import vibrate_motor


def handle_wake_up():
    # Initialize the buttons
    menu_btn = machine.Pin(MENU_BTN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    up_btn = machine.Pin(UP_BTN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    down_btn = machine.Pin(DOWN_BTN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
    back_btn = machine.Pin(BACK_BTN_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

    esp32.wake_on_ext1([menu_btn, up_btn,
                        down_btn,
                        back_btn], esp32.WAKEUP_ANY_HIGH)

    # Check the wake-up reason
    wake_reason = machine.wake_reason()

    if wake_reason == machine.EXT0_WAKE:
        print("First wake up")
    elif wake_reason == machine.EXT1_WAKE:
        print("Buttons wake up")
    elif wake_reason == machine.TIMER_WAKE:
        print("Timer wake up")
    else:
        print("Wake up was not caused by deep sleep")

    time.sleep(0.7)
    print('Going to sleep')
    vibrate_motor(200)
    machine.deepsleep(20000)


if __name__ == '__main__':
    handle_wake_up()
