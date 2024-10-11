import os
import random

from aiogram.types import InputFile
from aiogram.utils.markdown import quote_html

from config import Config, i18n

_ = i18n.gettext


class Messages:
    #  Статья с фото:  https://telegra.ph/YuumeSignals-08-10

    @staticmethod
    def get_welcome_sticker() -> str:
        return 'CAACAgIAAxkBAAECVgRmuN__Guzdwhhaedl0tD6YjMkvcgACTCgAAg95WUuuGnhFtULX4TUE'

    @staticmethod
    def get_choose_language_photo() -> str:
        return 'https://sun9-4.userapi.com/impg/EB3SeFC08ZmCRGfuxusRfDFlZbjpgH2b2GSK9g/ubAvMkT7Tmo.jpg?size=1280x720&quality=96&sign=f7b9f7f0dc836aa5c8dd663a8fdae1db&type=album'

    @staticmethod
    def get_choose_language() -> str:
        return 'Choose a language / Выберете язык / एक भाषा चुनें'

    @staticmethod
    def get_welcome(user_name: str) -> str:
        return _(
            '🎯 <b>Приветствую тебя, {user_name}!</b> \n\n'

            '🤖 В этом боте наша команда разместила софт на популярные мини-игры в онлайн казино. \n\n'

            '<b>Данный бот основан и обучен на нейросети</b> 🖥 [<code>OpenAI</code>]. \n\n'

            '<code>На текущий момент бот по сей день проходит проверки и  исправления! '
            'Точность бота составляет 89%!</code>'
        ).format(user_name=quote_html(user_name))

    @staticmethod
    def get_welcome_photo() -> str:
        return 'https://sun9-2.userapi.com/impg/VQRK-u5ZNNaeXSuInd4Et5V1Il9Sfve4SU8MRg/jiatzw-pKBQ.jpg?size=1280x720&quality=96&sign=30fb922d493abe5fbffc1e7d5c700830&type=album'

    @staticmethod
    def get_support() -> str:
        return _(
            'Если у вас появились какие либо вопросы, либо появились трудности при использовании бота, '
            'напишите нашему менеджеру - он с радостью вам поможет. \n\n'
            '<b>💬 Отвечаем всем, в порядке очереди.</b>'
        )

    @staticmethod
    def get_ask_for_subscribe() -> str:
        return _('<b>Для получения сигналов, нужно подписаться на основные каналы и проверить подписку</b> 👇🏻')

    @staticmethod
    def get_not_subscribed() -> str:
        return _('Подпишитесь на каналы❗️')

    @staticmethod
    def get_registration(user_id: int):
        return _(
            "Для того что связать аккаунт с нейросетью из софта следуйте инструкции: \n\n"

            "Создайте новый аккаунт в <a href='{registration_link}'>1WIN</a> по кнопке ниже, "
            "<b>введя промо «<code>{promo_code}</code>»</b> - "
            "он выдает доступ к сигналам и самый жирный бонус! \n\n"

            "<i>Если не открывается - заходим с включенным VPN</i> 🌐 \n\n"

            "📲 Если у вас нет номера для создания аккаунта, "
            "<b>можно использовать социальные сети, либо GMAIL почту.</b>"
        ).format(
            registration_link=Config.get_registration_link(user_id=user_id), 
            promo_code=Config.promo_code
        )

    @staticmethod
    def get_registration_photo():
        return _('registration_photo_url')
    
    @staticmethod
    def get_deposit_photo():
        return _('deposit_photo_url')

    @staticmethod
    def get_registration_not_passed():
        return _(
            '⚠️ Упс! Софт не видит аккаунт в базе. \n\n'

            '❗️Возможно, вы зарегистрировались не по ссылке, либо зашли в старый аккаунт. \n\n'

            '🎁 <b>Обязательно вводи промокод «<code>{promo_code}</code>» при регистрации!</b> \n\n'

            '<b>Это нужно для того, чтобы нейросеть из софта смогла вас определить</b> ✔'
        ).format(promo_code=Config.promo_code)

    @staticmethod
    def get_registration_passed():
        return _(
            "<b>Софт увидел ваш аккаунт! Остался последний шаг</b> ✅ \n\n"

            "Теперь пришло время пополнить ваш игровой счет в 1WIN, "
            "<b>чтобы бот мог начать выдавать сигналы</b>. \n\n"
            "🔓 После пополнения счета нажмите кнопку <b>«Проверить депозит»</b>, "
            "чтобы получить полный доступ к сигналам софта. \n\n"

            "<b>После активации автоматически выдается доступ к БОТУ</b> 🤖"
        )

    @staticmethod
    def get_deposit_not_found() -> str:
        return '❗️' + _('Ваш депозит не найден, пожалуйста попробуйте ещё раз.')

    @staticmethod
    def get_bot_activated() -> str:
        return _(
            "<b>ДОСТУП К СИГНАЛАМ АКТИВЕН</b> ✅ \n\n"
            "❗️<i>Выводим ДО кэфа который выдал бот</i> \n\n"
            "Для начала ознакомьтесь с обучением по кнопке ниже."
        )
    

    @staticmethod
    def get_guide() -> str:
        return _(
            "<i><b>С каждым пополнением % захода сигнала будем повышаться.</b></i> \n\n"

            "1 уровень - 25% захода сигнала \n"
            "2 уровень - 35% захода сигнала \n"
            "3 уровень - 45% захода сигнала \n"
            "4 уровень - 65% захода сигнала \n"
            "5 уровень - 80% захода сигнала \n"
            "6 уровень - 100% захода сигнала \n\n"
            
            "Что бы повысить уровень, вам надо сделать пополнение в размере 10$ (переводим в свою валюту) \n"
            " <b>1 пополнение - 1 уровень</b> \n\n"

            "<i><b>Это нужно для алгоритмов встроенных в нашего бота, просим прощения за неудобства</b></i> 🤝🏻"
        )
    
    @staticmethod
    def get_signal_photo(game_name: str = "aviator") -> str: 
        images_dir_path = "resources/aviator"
        files = [
            filename for filename in os.listdir(images_dir_path)
            if filename.endswith('.png') or filename.endswith('.jpg')
        ]

        random_filename = random.choice(files)
        image_path = os.path.join(images_dir_path, random_filename)
        return InputFile(image_path)
