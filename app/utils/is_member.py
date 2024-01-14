from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.types import Message, CallbackQuery

from app.database.models import User

from config import *


async def is_member(message: Message):
    user: User = User.get(
        telegram_id=message.from_user.id
    )

    member = await message.bot.get_chat_member(chat_id=AD_CHANNEL_ID, user_id=message.from_user.id)
    if member.status == ChatMemberStatus.LEFT:
        user.membered = False 
        user.save()
        return False

    if member.status != ChatMemberStatus.LEFT:
        user.membered = True 
        user.save()
        return True