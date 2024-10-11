import threading

from src.bot import start_bot
from src.postback import run_app
from src.utils import setup_logger


def run_app_thread():
    run_app()


def start_bot_thread():
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())


if __name__ == '__main__':
    setup_logger()

    # t1 = threading.Thread(target=run_app_thread)
    t2 = threading.Thread(target=start_bot_thread)

    # t1.start()
    t2.start()

    # t1.join()
    t2.join()
