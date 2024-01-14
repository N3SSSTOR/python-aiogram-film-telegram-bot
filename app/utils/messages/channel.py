from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from app.database.models import *

from config import *


async def channel(message: Message):
    user: User = User.get(
        telegram_id=message.from_user.id 
    )

    match user.lang:
        case "RU":
            await message.answer(
                text="Для работы с данным ботом нужно подписаться на спонсорский канал 👇👇👇",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Канал", url=AD_CHANNEL_URL)],
                    [InlineKeyboardButton(text="Подписался 👍", callback_data="i_subscribed")],
                ])
            )

        case "ENG":
            await message.answer(
                text="To work with this bot you need to subscribe to a sponsor channel 👇👇👇",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Channel", url=AD_CHANNEL_URL)],
                    [InlineKeyboardButton(text="Subscribed 👍", callback_data="i_subscribed")],
                ])
            )