from typing import Generator
from datetime import datetime, timedelta

from .models import User
from .reflink import increase_users_count


# region SQL Select


def get_users_total_count() -> int:
    return User.select().count()


def get_users_by_hours(hours: int):
    start_time = datetime.now() - timedelta(hours=hours)
    users_count = User.select().where(User.registration_timestamp >= start_time).count()

    return users_count


def get_user_ids() -> Generator:
    yield from (user.telegram_id for user in User.select())


def get_all_users() -> tuple:
    yield from ((user.telegram_id, user.name, user.referral_link, user.registration_timestamp, user.language_code, user.onewin_id) for user in User.select())


def get_user_or_none(telegram_id: int) -> User | None:
    return User.get_or_none(User.telegram_id == telegram_id)


def get_user_locale_or_none(telegram_id: int) -> str | None:
    try:
        return User.get(User.telegram_id == telegram_id).language_code
    except User.DoesNotExist:
        return None


def get_user_1win_id(telegram_id: int) -> int | None:
    user = get_user_or_none(telegram_id=telegram_id)
    if not user:
        return None
    return user.onewin_id


def get_user_by_1win_id(one_win_id: int) -> User | None:
    user = User.get_or_none(User.onewin_id == one_win_id)
    if not user:
        return None
    return user


# endregion


# region SQL Create

def create_or_update_user(telegram_id: int, name: str, reflink: str = None) -> None:
    user = get_user_or_none(telegram_id)

    if not user:
        User.create(name=name, telegram_id=telegram_id, referral_link=reflink)
        increase_users_count(reflink=reflink)
    else:
        user.update(name=name)
        user.save()

# endregion


# region Update


def set_user_1win_id(telegram_id: int, onewin_id: int):
    User.update(onewin_id=onewin_id).where(User.telegram_id == telegram_id).execute()


def set_locale(telegram_id: int, language_code: str) -> None:
    User.update(language_code=language_code).where(User.telegram_id == telegram_id).execute()

# endregion
