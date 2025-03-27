import machine
import esp32
import time
from constants import MENU_BTN_PIN, UP_BTN_PIN, DOWN_BTN_PIN, BACK_BTN_PIN
from utils import vibrate_motor, get_battery_voltage, battery_percentage
from display import Display
import fira_sans_regular_38
import fira_sans_regular_24
from constants import WHITE, BLACK


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

    display = Display()
    display.fill(WHITE)

    year, month, mday, hour, _min, sec, _, _ = time.localtime()
    display_time = "{:02d}:{:02d}:{:02d}".format(hour, _min, sec)
    display.display_text(
        display_time,
        int((int(Display.MAX_WIDTH/2)-len(display_time)) / 2),
        int(Display.MAX_HEIGHT/2),
        fira_sans_regular_38,
        WHITE,
        BLACK
    )
    
    v = get_battery_voltage()
    display.display_text(
        "V{:.2f} - {:02d}%".format(v, battery_percentage(v)),
        4, 4, fira_sans_regular_24,
        WHITE,
        BLACK
    )

    display.update()
    display.sleep()

    vibrate_motor([300])
    machine.deepsleep(120000)


if __name__ == '__main__':
    handle_wake_up()
