from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Menu")]],
        resize_keyboard=True
    )