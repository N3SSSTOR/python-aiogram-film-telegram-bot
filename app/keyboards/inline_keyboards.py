from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


# RU


back_to_main_menu_button = InlineKeyboardButton(
    text="Назад ⬅️",
    callback_data="back_to_main_menu"
)


def get_back_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [back_to_main_menu_button]
    ])

    return keyboard


def get_regenerate_captcha_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Перегенерировать 🔄",
            callback_data="regenerate_captcha"
        )]
    ])

    return keyboard


def get_main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Инструкция 📄", callback_data="help"),
            InlineKeyboardButton(text="Настройки ⚙️", callback_data="main_menu_settings")
        ],
        [
            InlineKeyboardButton(text="Моя подписка 👑", callback_data="main_menu_subscribe"),
            InlineKeyboardButton(text="Партнерам 🤝", callback_data="main_menu_partners")
        ],
        [InlineKeyboardButton(text="Найти фильм 🔎", switch_inline_query_current_chat="")],
    ])

    return keyboard


def get_main_menu_settings_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить язык 🌍", callback_data="change_lang")],
        [back_to_main_menu_button],
    ])

    return keyboard


def get_change_lang_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="RU 🇷🇺", callback_data="change_lang_ru"),
            InlineKeyboardButton(text="ENG 🇬🇧", callback_data="change_lang_eng")
        ],
        [back_to_main_menu_button],
    ])

    return keyboard


def get_main_menu_subscribe_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оформить подписку 👑", callback_data="order_subscribe")],
        [back_to_main_menu_button],
    ])

    return keyboard


def get_main_menu_partners_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Стать реферером 💸", callback_data="ref"),
        ],
        [back_to_main_menu_button],
    ])

    return keyboard  


def get_payed_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатил ✅", callback_data="payed")],
    ])

    return keyboard   


# ENG


eng_back_to_main_menu_button = InlineKeyboardButton(
    text="Back ⬅️",
    callback_data="back_to_main_menu"
)


def eng_get_back_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [eng_back_to_main_menu_button]
    ])

    return keyboard


def eng_get_regenerate_captcha_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Regenerate 🔄",
            callback_data="regenerate_captcha"
        )]
    ])

    return keyboard


def eng_get_main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Instructions 📄", callback_data="help"),
            InlineKeyboardButton(text="Settings ⚙️", callback_data="main_menu_settings")
        ],
        [
            InlineKeyboardButton(text="My subscribe 👑", callback_data="main_menu_subscribe"),
            InlineKeyboardButton(text="Partners 🤝", callback_data="main_menu_partners")
        ],
        [InlineKeyboardButton(text="Find film 🔎", switch_inline_query_current_chat="")],
    ])

    return keyboard


def eng_get_main_menu_settings_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Change language 🌍", callback_data="change_lang")],
        [eng_back_to_main_menu_button],
    ])

    return keyboard


def eng_get_change_lang_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="RU 🇷🇺", callback_data="change_lang_ru"),
            InlineKeyboardButton(text="ENG 🇬🇧", callback_data="change_lang_eng")
        ],
        [eng_back_to_main_menu_button],
    ])

    return keyboard


def eng_get_main_menu_subscribe_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Subscribe 👑", callback_data="order_subscribe")],
        [eng_back_to_main_menu_button],
    ])

    return keyboard


def eng_get_main_menu_partners_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Become a referrer 💸", callback_data="ref"),
            InlineKeyboardButton(text="Create bot 🖥", callback_data="copy_bot")
        ],
        [eng_back_to_main_menu_button],
    ])

    return keyboard  


def eng_get_payed_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Payed ✅", callback_data="payed")],
    ])

    return keyboard  