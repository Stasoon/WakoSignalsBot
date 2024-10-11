import gettext
import os
from contextvars import ContextVar
from typing import Any, Dict, Tuple, Optional

from babel import Locale
from babel.support import LazyProxy
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from src.database.users import get_user_or_none


class I18nMiddleware(BaseMiddleware):
    """
    I18n middleware based on gettext util
    """

    ctx_locale = ContextVar('ctx_user_locale', default=None)

    def __init__(self, domain, path=None, default='ru'):
        """
        :param domain: domain
        :param path: path where located all *.mo files
        :param default: default locale name
        """
        super(I18nMiddleware, self).__init__()

        if path is None:
            path = os.path.join(os.getcwd(), 'locales')

        self.domain = domain
        self.path = path
        self.default = default

        self.locales = self.find_locales()

    def find_locales(self) -> Dict[str, gettext.GNUTranslations]:
        """
        Load all compiled locales from path

        :return: dict with locales
        """
        translations = {}

        for name in os.listdir(self.path):
            if not os.path.isdir(os.path.join(self.path, name)):
                continue
            mo_path = os.path.join(self.path, name, 'LC_MESSAGES', self.domain + '.mo')

            if os.path.exists(mo_path):
                with open(mo_path, 'rb') as fp:
                    translations[name] = gettext.GNUTranslations(fp)
            elif os.path.exists(mo_path[:-2] + 'po'):
                raise RuntimeError(f"Found locale '{name}' but this language is not compiled!")

        return translations

    def change_locale_context(self, lang_code: str):
        if lang_code not in self.available_locales:
            return
        self.ctx_locale.set(lang_code)

    def reload(self):
        """
        Hot reload locales
        """
        self.locales = self.find_locales()

    @property
    def available_locales(self) -> Tuple[str]:
        """
        list of loaded locales

        :return:
        """
        return tuple(self.locales.keys())

    def __call__(self, singular, plural=None, n=1, locale=None) -> str:
        return self.gettext(singular, plural, n, locale)

    def gettext(self, singular, plural=None, n=1, locale=None) -> str:
        """
        Get text

        :param singular:
        :param plural:
        :param n:
        :param locale:
        :return:
        """
        if locale is None:
            locale = self.ctx_locale.get()

        if locale not in self.locales:
            if n == 1:
                return singular
            return plural

        translator = self.locales[locale]

        if plural is None:
            return translator.gettext(singular)
        return translator.ngettext(singular, plural, n)

    def lazy_gettext(self, singular, plural=None, n=1, locale=None, enable_cache=False) -> LazyProxy:
        """
        Lazy get text

        :param singular:
        :param plural:
        :param n:
        :param locale:
        :param enable_cache:
        :return:
        """
        return LazyProxy(self.gettext, singular, plural, n, locale, enable_cache=enable_cache)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        """
        User locale getter
        You can override the method if you want to use different way of
        getting user language.

        :param action: event name
        :param args: event arguments
        :return: locale name or None
        """
        user: Optional[types.User] = types.User.get_current()

        if not user or not user.id:
            return self.default

        # Если язык сохранён в БД, используем его
        db_user = get_user_or_none(user.id)
        if db_user:
            lang_code = db_user.language_code
        else:
            lang_code = self.default

        if lang_code and lang_code in self.available_locales:
            return lang_code

        # Иначе берём язык, который установил телеграм
        locale: Optional[Locale] = user.locale if user else None
        if locale and locale.language in self.locales:
            *_, data = args
            language = data['locale'] = locale.language

            db_user.language_code = language
            db_user.save()
            return language

        # Иначе ставим дефолтный
        db_user.language_code = self.default
        db_user.save()
        return self.default

    async def trigger(self, action, args):
        """
        Event trigger

        :param action: event name
        :param args: event arguments
        :return:
        """
        if (
            'update' not in action
            and 'error' not in action
            and action.startswith('pre_process')
        ):
            locale = await self.get_user_locale(action, args)
            self.change_locale_context(locale)
            return True
