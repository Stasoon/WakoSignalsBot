from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.callback_data import CallbackData

from config import Config, i18n

_ = i18n.gettext


class Keyboards:
    locale_callback_data = CallbackData('locale', 'language_code')
    deposit_check_callback = CallbackData('check_dep', 'one_win_id')
    language_callback = CallbackData('language', 'lang_code')

    @classmethod
    def get_choose_language(cls):
        markup = InlineKeyboardMarkup(row_width=3, resize_keyboard=True, is_persistent=True)

        ru = InlineKeyboardButton('🇷🇺 Русский', callback_data=cls.language_callback.new(lang_code='ru'))
        en = InlineKeyboardButton('🇺🇸 English', callback_data=cls.language_callback.new(lang_code='en'))
        hi = InlineKeyboardButton("🇮🇳 भारत", callback_data=cls.language_callback.new(lang_code="hi"))

        return markup.add(en, ru, hi)

    @staticmethod
    def get_welcome_menu() -> InlineKeyboardMarkup:
        next_button = InlineKeyboardButton(text=_('📲 Получить софт'), callback_data='next')
        lang_button = InlineKeyboardButton(text=_('🌐 Сменить язык'), callback_data='change_lang')
        support_button = InlineKeyboardButton(text=_('⚙️ Поддержка'), callback_data='support')
        channel_button = InlineKeyboardButton(text=_('🔈 Канал'), url=Config.CHANNELS_TO_SUB[0].get('url'))
        return InlineKeyboardMarkup(row_width=1).add(next_button, lang_button).row(channel_button, support_button)

    @staticmethod
    def get_support() -> InlineKeyboardMarkup:
        support_button = InlineKeyboardButton(text=_('✍️ Написать менеджеру'), url=Config.SUPPORT_URL)
        menu_button = InlineKeyboardButton(text=_('🔙 Главное меню'), callback_data='menu')
        return InlineKeyboardMarkup(row_width=1).add(support_button, menu_button)

    @staticmethod
    def get_channels_to_subscribe(lang_code: str) -> InlineKeyboardMarkup:
        channel_buttons = []
        # channels_to_sub = filter(lambda c: c.get('lang') == lang_code, Config.CHANNELS_TO_SUB)

        for n, channel in enumerate(Config.CHANNELS_TO_SUB, start=1):
            channel_buttons.append(
                InlineKeyboardButton(text=_('📲 Подписаться на {n}-й канал').format(n=n), url=channel.get('url'))
            )
        check = InlineKeyboardButton(text='♻️ '+_('Проверить подписку')+' ♻️', callback_data='check_sub')

        return InlineKeyboardMarkup(row_width=1).add(*channel_buttons, check)

    @staticmethod
    def get_check_registration(user_id: int) -> InlineKeyboardMarkup:
        reg = InlineKeyboardButton(text='🔑 '+_('Регистрация'), url=Config.get_registration_link(user_id=user_id))
        check = InlineKeyboardButton(text='🔎 '+_('Проверить регистрацию'), callback_data='check_registration')
        menu_button = InlineKeyboardButton(text=_('🔙 Главное меню'), callback_data='menu')
        return InlineKeyboardMarkup(row_width=1).add(reg, check, menu_button)

    @staticmethod
    def get_check_deposit(user_id) -> InlineKeyboardMarkup:
        deposit = InlineKeyboardButton(
            text='💰 '+_('Пополнить баланс'),
            url=Config.get_registration_link(user_id=user_id)
        )
        check = InlineKeyboardButton(text='🔐 '+_('Проверить депозит'), callback_data='check_deposit')

        menu_button = InlineKeyboardButton(text=_('🔙 Главное меню'), callback_data='menu')
        return InlineKeyboardMarkup(row_width=1).add(deposit, check, menu_button)

    @staticmethod
    def get_play(lang: str = "en") -> InlineKeyboardMarkup:
        game_url = f"https://stasmoons.github.io/WAKO/index.html?lang={lang}"
        play = InlineKeyboardButton(text="🗂️ WAKO | AI SOFT", web_app=WebAppInfo(url=game_url))

        aviator = InlineKeyboardButton(text="✈️ WAKO I AI AVIATOR", callback_data="aviator")

        menu_button = InlineKeyboardButton(text=_("🔙 Главное меню"), callback_data="menu")

        return InlineKeyboardMarkup(row_width=1).add(play, aviator, menu_button)

    @staticmethod
    def get_guide_and_play(lang: str = "en") -> InlineKeyboardMarkup:
        guide = InlineKeyboardButton(text=_("📚 Обучение"), callback_data="guide")

        game_url = f"https://stasmoons.github.io/WAKO/index.html?lang={lang}"
        play = InlineKeyboardButton(text="🗂️ WAKO | AI SOFT", web_app=WebAppInfo(url=game_url))

        aviator = InlineKeyboardButton(text="✈️ WAKO I AI AVIATOR", callback_data="aviator")

        menu_button = InlineKeyboardButton(text=_("🔙 Главное меню"), callback_data="menu")

        return InlineKeyboardMarkup(row_width=1).add(guide, play, aviator, menu_button)
    
    @staticmethod
    def get_next_signal(game: str = "aviator") -> InlineKeyboardMarkup:
        signal_button = InlineKeyboardButton(text=_("✈️ Следующий сигнал"), callback_data=game)
        menu_button = InlineKeyboardButton(text=_("🔙 Главное меню"), callback_data="menu")
        return InlineKeyboardMarkup(row_width=1).add(signal_button, menu_button)

