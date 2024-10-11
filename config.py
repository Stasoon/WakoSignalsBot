import os
from typing import Final
from dotenv import load_dotenv, find_dotenv

from src.middlewares.i18n import I18nMiddleware

load_dotenv(find_dotenv())

i18n = I18nMiddleware(domain='messages', path='locales', default='ru')


class Config:
    BOT_TOKEN: Final = os.getenv('BOT_TOKEN', 'Впишите токен в .env!')
    ADMIN_IDS: Final = tuple(int(i) for i in str(os.getenv('BOT_ADMIN_IDS')).split(','))

    POSTBACK_PORT: Final = int(os.getenv('POSTBACK_PORT'))
    POSTBACK_BOT_TOKEN: Final = os.getenv('POSTBACK_BOT_TOKEN')
    REGISTRATION_URL = os.getenv('ONE_WIN_REGISTRATION_URL')

    SUPPORT_URL = os.getenv('SUPPORT_URL')

    CHANNELS_TO_SUB = (
        {'id': -1002187009580, 'url': 'https://t.me/+X14cve8XmK1jNDI6'},
        {'id': -1002203959521, 'url': 'https://t.me/+chrnhqpalKNhZDQy'},
    )

    promo_code = 'BOOST66'

    @classmethod
    def get_registration_link(cls, user_id: int):
        return f"{cls.REGISTRATION_URL}&sub1={user_id}"

