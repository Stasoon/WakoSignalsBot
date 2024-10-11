import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatMemberStatus, ChatJoinRequest
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import BadRequest, RetryAfter
from loguru import logger

from config import i18n, Config
from src.database import users
from src.database.models import OneWinRegistration, OneWinDeposit
from src.database.one_win_deposits import get_user_deposits_summ
from src.utils import send_typing_action
from .messages import Messages
from .kb import Keyboards
from src.database.models import ChannelJoinRequest
from src.create_bot import bot


# region Utils

async def is_user_subscribed_on_channel(user_id: int, channel_id: int) -> bool:
    """ Проверить, подписан ли пользователь на канал / подавал ли заявку """
    if ChannelJoinRequest.get_or_none(user_id=user_id, channel_id=channel_id):
        return True

    try:
        channel_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    except (BadRequest, RetryAfter) as e:
        logger.error(e)
        return True
    except Exception:
        return False

    if channel_member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        return False
    return True


async def is_user_subscribed(user_id) -> bool:
    channels_subscriptions = [
        await is_user_subscribed_on_channel(user_id=user_id, channel_id=channel.get('id'))
        for channel in Config.CHANNELS_TO_SUB
    ]
    return all(channels_subscriptions)


async def __send_language_choice(to_message: Message):
    await to_message.answer_photo(
        photo=Messages.get_choose_language_photo(),
        caption=Messages.get_choose_language(),
        reply_markup=Keyboards.get_choose_language()
    )


async def __send_main_menu(user_id: int, user_first_name: str):
    await bot.send_photo(
        chat_id=user_id,
        photo=Messages.get_welcome_photo(),
        caption=Messages.get_welcome(user_first_name),
        reply_markup=Keyboards.get_welcome_menu()
    )


async def __send_deposit(user_id: int):
    text = Messages.get_registration_passed()
    photo = Messages.get_deposit_photo()
    markup = Keyboards.get_check_deposit(user_id=user_id)
    await bot.send_photo(chat_id=user_id, caption=text, photo=photo, reply_markup=markup)


# endregion


# region Handlers


async def handle_join_request(update: ChatJoinRequest):
    ChannelJoinRequest.get_or_create(user_id=update.from_user.id, channel_id=update.chat.id)


async def handle_start_command(message: Message, state: FSMContext) -> None:
    await state.finish()
    await send_typing_action(message)

    await message.answer_sticker(sticker=Messages.get_welcome_sticker())
    await asyncio.sleep(0.5)

    users.create_or_update_user(
        telegram_id=message.from_id,
        name=message.from_user.username or message.from_user.full_name,
        reflink=message.get_full_command()[1]
    )

    await __send_language_choice(to_message=message)


async def handle_language_choice_callback(callback: CallbackQuery, callback_data):
    await callback.answer()
    lang_code = callback_data.get('lang_code')

    user = users.get_user_or_none(telegram_id=callback.from_user.id)
    user.language_code = lang_code
    user.save()

    i18n.change_locale_context(lang_code)

    is_user_sub = await is_user_subscribed(user_id=callback.from_user.id)
    if not is_user_sub:
        user = users.get_user_or_none(telegram_id=callback.from_user.id)
        text = Messages.get_ask_for_subscribe()
        markup = Keyboards.get_channels_to_subscribe(lang_code=user.language_code)
        await callback.message.answer(text=text, reply_markup=markup)
    else:
        await __send_main_menu(user_id=user.telegram_id, user_first_name=callback.from_user.first_name)

    await callback.message.delete()


async def handle_check_subscription(callback: CallbackQuery):
    is_user_sub = await is_user_subscribed(user_id=callback.from_user.id)
    if not is_user_sub:
        await callback.answer(text=Messages.get_not_subscribed(), show_alert=True)
        return

    await send_typing_action(callback.message)
    await callback.answer('✅')

    await __send_main_menu(user_id=callback.from_user.id, user_first_name=callback.from_user.first_name)
    await callback.message.delete()


async def handle_change_lang(callback: CallbackQuery):
    await __send_language_choice(to_message=callback.message)
    await callback.message.delete()


async def handle_support(callback: CallbackQuery):
    await callback.message.answer_photo(
        photo=Messages.get_welcome_photo(), caption=Messages.get_support(), reply_markup=Keyboards.get_support()
    )
    await callback.message.delete()


async def handle_back_to_menu(callback: CallbackQuery):
    await __send_main_menu(user_id=callback.from_user.id, user_first_name=callback.from_user.first_name)
    await callback.message.delete()


async def handle_next(callback: CallbackQuery):
    await callback.answer()
    user = users.get_user_or_none(telegram_id=callback.from_user.id)
    
    if not user.onewin_id or get_user_deposits_summ(user.onewin_id) == 0:
        await callback.message.answer_photo(
            photo=Messages.get_registration_photo(),
            caption=Messages.get_registration(user_id=callback.from_user.id),
            reply_markup=Keyboards.get_check_registration(callback.from_user.id),
        )
        return

    await callback.message.answer(
        text=Messages.get_bot_activated(),
        reply_markup=Keyboards.get_guide_and_play(lang=user.language_code)
    )


async def handle_check_registration(callback: CallbackQuery):
    one_win_registration = OneWinRegistration.get_or_none(OneWinRegistration.sub1 == callback.from_user.id)

    if not one_win_registration:
        await callback.answer()
        await callback.message.answer(
            text=Messages.get_registration_not_passed(),
            reply_markup=Keyboards.get_check_registration(user_id=callback.from_user.id)
        )
    else:
        await callback.answer('✅')
        await __send_deposit(user_id=callback.from_user.id)

        user = users.get_user_or_none(telegram_id=callback.from_user.id)
        user.onewin_id = one_win_registration.one_win_id
        user.save()

    await callback.message.delete()


async def handle_check_deposit(callback: CallbackQuery):
    user = users.get_user_or_none(telegram_id=callback.from_user.id)

    if not user.onewin_id or get_user_deposits_summ(user.onewin_id) == 0:
        await callback.answer(text=Messages.get_deposit_not_found(), show_alert=True)
    else:
        await callback.answer()
        await callback.message.answer(
            text=Messages.get_bot_activated(),
            reply_markup=Keyboards.get_guide_and_play(lang=user.language_code)
        )
        await callback.message.delete()

    
async def handle_get_aviator_signal(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer_photo(
        photo=Messages.get_signal_photo(),
        reply_markup=Keyboards.get_next_signal(game="aviator")
    )


async def handle_guide(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        text=Messages.get_guide(),
        reply_markup=Keyboards.get_play()
    )


# endregion


def register_user_handlers(dp: Dispatcher) -> None:
    # обработка заявки в канал
    dp.register_chat_join_request_handler(handle_join_request)

    # обработка команды /start
    dp.register_message_handler(handle_start_command, commands=['start'], state='*')

    dp.register_callback_query_handler(handle_language_choice_callback, Keyboards.language_callback.filter())

    dp.register_callback_query_handler(handle_next, text='next')
    dp.register_callback_query_handler(handle_change_lang, text='change_lang')
    dp.register_callback_query_handler(handle_support, text='support')
    dp.register_callback_query_handler(handle_back_to_menu, text='menu')

    dp.register_callback_query_handler(handle_check_subscription, text='check_sub')

    # регистрация
    dp.register_callback_query_handler(handle_check_registration, text='check_registration')

    dp.register_callback_query_handler(handle_check_deposit, text='check_deposit')

    dp.register_callback_query_handler(handle_get_aviator_signal, text="aviator")

    dp.register_callback_query_handler(handle_guide, text="guide")

