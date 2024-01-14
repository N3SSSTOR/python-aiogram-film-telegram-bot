from aiogram.types import Message, CallbackQuery

from app.database.models import User
from app.keyboards.inline_keyboards import *
from app.utils.get_user_profile_text import get_user_profile_text
from app.utils.messages.channel import channel
from app.utils.is_member import is_member


async def send_main_menu_message(message: Message):
    await is_member(message=message)

    user: User = User.get(
        telegram_id=message.from_user.id
    )    

    if user.membered:
        match user.lang:
            case "RU":
                await message.answer(
                    reply_markup=get_main_menu_keyboard(),
                    text=get_user_profile_text(message=message)
                )

            case "ENG":
                await message.answer(
                    reply_markup=eng_get_main_menu_keyboard(),
                    text=get_user_profile_text(message=message)
                )

    else:
        await channel(message=message)