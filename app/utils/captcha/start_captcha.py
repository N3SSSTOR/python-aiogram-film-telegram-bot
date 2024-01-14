import os

from aiogram.types import Message, CallbackQuery
from aiogram.types.input_file import FSInputFile

from app.database.models import User
from app.utils.captcha.create_captcha import create_captcha
from app.keyboards.inline_keyboards import get_regenerate_captcha_keyboard


async def start_captcha(message: Message | None = None, callback: CallbackQuery | None = None):
    captcha_text, path = create_captcha()

    if message:
        telegram_id = message.from_user.id 

    if callback:
        telegram_id = callback.from_user.id

    user: User = User.get(
        telegram_id=telegram_id
    )
    user.captcha_text = captcha_text
    user.save()

    photo = FSInputFile(path)

    if message:
        match user.lang:
            case "RU":
                await message.answer_photo(
                    photo=photo,
                    caption="<em>Чтобы доказать что вы не робот введите текст с картинки</em>",
                    reply_markup=get_regenerate_captcha_keyboard()
                )

            case "ENG":
                await message.answer_photo(
                    photo=photo,
                    caption="<em>To prove that you are not a robot, enter the text from the image</em>",
                    reply_markup=get_regenerate_captcha_keyboard()
                )          

    if callback:
        match user.lang:
            case "RU":
                await callback.message.answer_photo(
                    photo=photo,
                    caption="<em>Чтобы доказать что вы не робот введите текст с картинки</em>",
                    reply_markup=get_regenerate_captcha_keyboard()
                )      

            case "ENG":
                await callback.message.answer_photo(
                    photo=photo,
                    caption="<em>To prove that you are not a robot, enter the text from the image</em>",
                    reply_markup=get_regenerate_captcha_keyboard()
                )      

    os.remove(path)