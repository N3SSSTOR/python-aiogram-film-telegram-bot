from aiogram import Bot, Dispatcher 
from aiogram.types import BotCommand

from app.handlers.message_handlers import message_router
from app.handlers.callback_handlers import callback_router
from app.handlers.inline_query_handlers import inline_query_router


async def run_user_bot(token):
    bot2 = Bot(
        token=token,
        parse_mode="HTML" 
    )

    dp2 = Dispatcher()
    dp2.include_router(message_router)
    dp2.include_router(callback_router)
    dp2.include_router(inline_query_router)

    bot_commands = [
        BotCommand(command="/help", description="Инструкция 📄"),
        BotCommand(command="/menu", description="Меню 📋"),
        BotCommand(command="/find", description="Найти контент по тегам 🔍"),
    ]
    await bot2.set_my_commands(bot_commands)

    await dp2.start_polling(bot2)