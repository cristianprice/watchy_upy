from rtc import WatchyRTC
import asyncio


async def main():
    rtc = WatchyRTC()

    while True:
        await asyncio.sleep(0.1)
        await rtc.set_now()
        await asyncio.sleep(1)
        print(await rtc.get_time())
        await rtc.set_now()
        await asyncio.sleep(1)



asyncio.run(main())
