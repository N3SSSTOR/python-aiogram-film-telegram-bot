import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher 
from aiogram.types import BotCommand

from config import TELEGRAM_BOT_TOKEN
from app.handlers.message_handlers import message_router
from app.handlers.callback_handlers import callback_router
from app.handlers.inline_query_handlers import inline_query_router


async def main(token=TELEGRAM_BOT_TOKEN):
    bot = Bot(
        token=token,
        parse_mode="HTML" 
    )

    dp = Dispatcher()
    dp.include_router(message_router)
    dp.include_router(callback_router)
    dp.include_router(inline_query_router)

    bot_commands = [
        BotCommand(command="/help", description="Инструкция 📄"),
        BotCommand(command="/menu", description="Меню 📋"),
        BotCommand(command="/find", description="Найти контент по тегам 🔍"),
    ]
    await bot.set_my_commands(bot_commands)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())

    except KeyboardInterrupt:
        print(f"\nExit")