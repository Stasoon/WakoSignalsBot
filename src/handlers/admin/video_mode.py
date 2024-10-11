from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Message

from src.misc.admin_states import VideoMode


class Keyboards:
    reply_button_for_admin_menu = KeyboardButton('🖼 Фотографии для видео 🖼')

    done_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="✅ Готово"), KeyboardButton(text="❌ Отменить")]],
        resize_keyboard=True, row_width=1
    )


async def handle_button(message: Message, state: FSMContext):
    await message.answer('Загрузите фотографии. Затем нажмите кнопку Готово:', reply_markup=Keyboards.done_kb)
    await state.set_state(VideoMode.wait_for_image)


async def handle_image(message: Message, state: FSMContext):
    data = await state.get_data()
    image_file_ids = data.get('image_file_ids')

    if not image_file_ids:
        image_file_ids = []

    image_file_ids.append(message.photo[0].file_id)
    await state.update_data(image_file_ids=image_file_ids)


async def handle_done_button(message: Message, state: FSMContext):
    image_file_ids = (await state.get_data()).get('image_file_ids')

    if not image_file_ids:
        await message.answer('Вы не добавили ни одного фото!')
        return

    with open('video_images.txt', 'w') as file:
        for file_id in image_file_ids:
            file.write(f"{file_id}\n")
    await message.answer('✅ Фотографии сохранены', reply_markup=ReplyKeyboardRemove())
    await state.finish()


async def handle_cancel_button(message: Message, state: FSMContext):
    await message.answer('Отменено', reply_markup=ReplyKeyboardRemove())
    await state.finish()


def register_video_mode_handlers(dp: Dispatcher):
    dp.register_message_handler(handle_button, lambda msg: msg.text == Keyboards.reply_button_for_admin_menu.text)
    dp.register_message_handler(handle_image, content_types=['photo'], state=VideoMode.wait_for_image)
    dp.register_message_handler(handle_done_button, lambda msg: msg.text == '✅ Готово', state=VideoMode.wait_for_image)
    dp.register_message_handler(handle_cancel_button, lambda msg: msg.text == '❌ Отменить', state=VideoMode.wait_for_image)
