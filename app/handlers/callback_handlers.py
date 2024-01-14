from aiogram import Router, F 
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.fsm.context import FSMContext

from app.utils.captcha.start_captcha import start_captcha
from app.utils.get_user_profile_text import get_user_profile_text
from app.utils.messages.main_menu_message import send_main_menu_message
from app.keyboards.inline_keyboards import *
from app.database.models import User
from app.fsm.token_states import TokenStates

from config import *


callback_router = Router()


@callback_router.callback_query(F.data == "copy_bot", StateFilter(None))
async def copy_bot(callback: CallbackQuery, state: FSMContext):
    user: User = User.get(
        telegram_id=callback.from_user.id 
    )

    await state.set_state(TokenStates.token)

    match user.lang:
        case "RU":
            await callback.message.answer(
                "<em>Введите токен бота</em>"
            )

        case "ENG":
            await callback.message.answer(
                "<em>Enter bot token</em>"
            )
    

@callback_router.callback_query(F.data == "i_subscribed")
async def i_subscribed(callback: CallbackQuery):
    user: User = User.get(
        telegram_id=callback.from_user.id
    )
    
    member = await callback.message.bot.get_chat_member(chat_id=AD_CHANNEL_ID, user_id=callback.from_user.id)
    if member.status == ChatMemberStatus.LEFT:
        await callback.message.reply(
            "👎"
        )

    if member.status != ChatMemberStatus.LEFT:
        await callback.message.reply(
            "👍",
            # reply_markup=main_reply_keyboard()
        )
        user.membered = True 
        user.save()

        match user.lang:
            case "RU":
                await callback.message.answer(
                    text=f"📄 <b>Инструкция по использованию бота</b>" + \
                    f"\n\n/help -  Инструкция 📄" + \
                    f"\n/menu -  Меню 📋" + \
                    f"\n\n/find - Найти контент по тегам 🔍 <em>(ниже примеры)</em>" + \
                    f"\n/find <em>слово пацана</em> ✅" + \
                    f"\n/find <em>Слово пацана. Кровь на асфальте</em> ✅" + \
                    f"\n/find <em>найди сериал слово пацана</em> ❌" + \
                    f"\n/find <em>слово пацана смотреть</em> ❌",
                    reply_markup=get_back_keyboard()
                )

            case "ENG":
                await callback.message.answer(
                    text=f"📄 <b>Instructions for using the bot</b>" + \
                    f"\n\n/help -  Instructions 📄" + \
                    f"\n/menu -  Menu 📋" + \
                    f"\n\n/find - Find content by tags 🔍 <em>(below are examples)</em>" + \
                    f"\n/find <em>breaking bad</em> ✅" + \
                    f"\n/find <em>Breaking Bad</em> ✅" + \
                    f"\n/find <em>find breaking bad</em> ❌" + \
                    f"\n/find <em>breaking bad online free</em> ❌",
                    reply_markup=eng_get_back_keyboard()
                )   


@callback_router.callback_query(F.data == "regenerate_captcha")
async def regenerate_captcha(callback: CallbackQuery):
    await callback.message.delete()
    await start_captcha(callback=callback)


@callback_router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu(callback: CallbackQuery):
    user: User = User.get(
        telegram_id=callback.from_user.id 
    )

    match user.lang:
        case "RU":
            await callback.message.edit_text(
                text=get_user_profile_text(callback=callback),
                reply_markup=get_main_menu_keyboard()
            )

        case "ENG":
            await callback.message.edit_text(
                text=get_user_profile_text(callback=callback),
                reply_markup=eng_get_main_menu_keyboard()
            )


@callback_router.callback_query(F.data == "main_menu_settings")
async def main_menu_settings(callback: CallbackQuery):
    user: User = User.get(
        telegram_id=callback.from_user.id 
    )

    match user.lang:
        case "RU":
            await callback.message.edit_text(
                text=f"⚙️ Настройки пользователя <b>{callback.from_user.first_name}</b> 👤",
                reply_markup=get_main_menu_settings_keyboard()
            )

        case "ENG":
            await callback.message.edit_text(
                text=f"⚙️ User settings <b>{callback.from_user.first_name}</b> 👤",
                reply_markup=eng_get_main_menu_settings_keyboard()
            )


@callback_router.callback_query(F.data == "change_lang")
async def main_menu_settings(callback: CallbackQuery):
    user: User = User.get(
        telegram_id=callback.from_user.id 
    )

    match user.lang:
        case "RU":
            await callback.message.edit_text(
                text=f"<em>Доступные языки:</em>" + \
                    f"\n\n🇷🇺 <b>RU</b> - <em>Русский</em>" + \
                    f"\n🇬🇧 <b>ENG</b> - <em>Английский</em>",
                reply_markup=get_change_lang_keyboard()
            )

        case "ENG":
            await callback.message.edit_text(
                text=f"<em>Available languages:</em>" + \
                    f"\n\n🇷🇺 <b>RU</b> - <em>Russian</em>" + \
                    f"\n🇬🇧 <b>ENG</b> - <em>English</em>",
                reply_markup=eng_get_change_lang_keyboard()
            )


@callback_router.callback_query(F.data == "change_lang_ru")
async def main_menu_settings(callback: CallbackQuery):
    user: User = User.get(
        telegram_id=callback.from_user.id
    )
    user.lang = "RU"

    user.save()

    await callback.answer("Язык изменен!")
    await callback.message.edit_text(
        text=get_user_profile_text(callback=callback),
        reply_markup=get_main_menu_keyboard()
    )


@callback_router.callback_query(F.data == "change_lang_eng")
async def main_menu_settings(callback: CallbackQuery):
    user: User = User.get(
        telegram_id=callback.from_user.id
    )
    user.lang = "ENG"

    user.save()

    await callback.answer("Language changed!")
    await callback.message.edit_text(
        text=get_user_profile_text(callback=callback),
        reply_markup=eng_get_main_menu_keyboard()
    )


@callback_router.callback_query(F.data == "main_menu_subscribe")
async def main_menu_settings(callback: CallbackQuery):
    user: User = User.get(
        telegram_id=callback.from_user.id
    )

    if user.subscribe_status:
        match user.lang:
            case "RU":
                await callback.message.edit_text(
                    text=f"<em>Ваша подписка <b>Активна</b></em> 🔥",
                    reply_markup=get_back_keyboard()
                )

            case "ENG":
                await callback.message.edit_text(
                    text=f"<em>Your subscribe <b>Active</b></em> 🔥",
                    reply_markup=eng_get_back_keyboard()
                )

    else:
        match user.lang:
            case "RU":
                await callback.message.edit_text(
                    text=f"<em>Ваша подписка <b>Неактивна</b></em> 😐",
                    reply_markup=get_main_menu_subscribe_keyboard()
                )

            case "ENG":
                await callback.message.edit_text(
                    text=f"<em>Your subscribe <b>Inactive</b></em> 😐",
                    reply_markup=eng_get_main_menu_subscribe_keyboard()
                )


@callback_router.callback_query(F.data == "main_menu_partners")
async def main_menu_partners(callback: CallbackQuery):
    user: User = User.get(
        telegram_id=callback.from_user.id
    )

    match user.lang:
        case "RU":
            await callback.message.edit_text(
                text=f"<em>Станьте нашим <b>партнером</b></em> 🤝💸",
                reply_markup=get_main_menu_partners_keyboard()
            )

        case "ENG":
            await callback.message.edit_text(
                text=f"<em>Become ours <b>partner</b></em> 🤝💸",
                reply_markup=eng_get_main_menu_partners_keyboard()
            )


@callback_router.callback_query(F.data == "order_subscribe")
async def order_subscribe(callback: CallbackQuery):
    try:
        user: User = User.get(
            telegram_id=callback.from_user.id
        )

        match user.lang:
            case "RU":
                await callback.message.edit_text(
                    text=get_user_profile_text(callback=callback),
                    reply_markup=get_main_menu_keyboard()
                )

            case "ENG":
                await callback.message.edit_text(
                    text=get_user_profile_text(callback=callback),
                    reply_markup=eng_get_main_menu_keyboard()
                )

        match user.lang:
            case "RU":
                match user.wait_check:
                    case 0:
                        await callback.message.answer(
                            text="<em>Совершите оплату</em>",
                            reply_markup=get_payed_keyboard()
                        )

                    case 1:
                        await callback.message.answer(
                            text="<em>Отправьте скриншот подтверждающий оплату</em>",
                        )       

                    case 2:
                        await callback.message.answer(
                            text="<em>Ваш платеж находится на проверке...</em>",
                        )          

            case "ENG":
                match user.wait_check:
                    case 0:
                        await callback.message.answer(
                            text="<em>Make a payment</em>",
                            reply_markup=eng_get_payed_keyboard()
                        )

                    case 1:
                        await callback.message.answer(
                            text="<em>Send a screenshot confirming payment</em>",
                        )       

                    case 2:
                        await callback.message.answer(
                            text="<em>Your payment is being verified...</em>",
                        )  

    except TelegramBadRequest:
        user: User = User.get(
            telegram_id=callback.from_user.id
        )

        match user.lang:
            case "RU":
                await callback.message.answer(
                    text=get_user_profile_text(callback=callback),
                    reply_markup=get_main_menu_keyboard()
                )

            case "ENG":
                await callback.message.answer(
                    text=get_user_profile_text(callback=callback),
                    reply_markup=eng_get_main_menu_keyboard()
                )

        match user.lang:
            case "RU":
                match user.wait_check:
                    case 0:
                        await callback.message.answer(
                            text="<em>Совершите оплату</em>",
                            reply_markup=get_payed_keyboard()
                        )

                    case 1:
                        await callback.message.answer(
                            text="<em>Отправьте скриншот подтверждающий оплату</em>",
                        )       

                    case 2:
                        await callback.message.answer(
                            text="<em>Ваш платеж находится на проверке...</em>",
                        )          

            case "ENG":
                match user.wait_check:
                    case 0:
                        await callback.message.answer(
                            text="<em>Make a payment</em>",
                            reply_markup=eng_get_payed_keyboard()
                        )

                    case 1:
                        await callback.message.answer(
                            text="<em>Send a screenshot confirming payment</em>",
                        )       

                    case 2:
                        await callback.message.answer(
                            text="<em>Your payment is being verified...</em>",
                        )           


@callback_router.callback_query(F.data == "payed")
async def payed(callback: CallbackQuery):
    user: User = User.get(
        telegram_id=callback.from_user.id
    )
    user.wait_check = 1

    user.save()

    match user.lang:
        case "RU":
            await callback.message.edit_text(
                text="<em>Отправьте скриншот подтверждающий оплату</em>"
            )

        case "ENG":
            await callback.message.edit_text(
                text="<em>Send a screenshot confirming payment</em>"
            )


@callback_router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    user: User = User.get(
        telegram_id=callback.from_user.id
    )

    match user.lang:
        case "RU":
            await callback.message.edit_text(
                text=f"📄 <b>Инструкция по использованию бота</b>" + \
                f"\n\n/help -  Инструкция 📄" + \
                f"\n/menu -  Меню 📋" + \
                f"\n\n/find - Найти контент по тегам 🔍 <em>(ниже примеры)</em>" + \
                f"\n/find <em>слово пацана</em> ✅" + \
                f"\n/find <em>Слово пацана. Кровь на асфальте</em> ✅" + \
                f"\n/find <em>найди сериал слово пацана</em> ❌" + \
                f"\n/find <em>слово пацана смотреть</em> ❌",
                reply_markup=get_back_keyboard()
            )

        case "ENG":
            await callback.message.edit_text(
                text=f"📄 <b>Instructions for using the bot</b>" + \
                f"\n\n/help -  Instructions 📄" + \
                f"\n/menu -  Menu 📋" + \
                f"\n\n/find - Find content by tags 🔍 <em>(below are examples)</em>" + \
                f"\n/find <em>breaking bad</em> ✅" + \
                f"\n/find <em>Breaking Bad</em> ✅" + \
                f"\n/find <em>find breaking bad</em> ❌" + \
                f"\n/find <em>breaking bad online free</em> ❌",
                reply_markup=eng_get_back_keyboard()
            )


@callback_router.callback_query(F.data == "ref")
async def ref(callback: CallbackQuery):
    user: User = User.get(
        telegram_id=callback.from_user.id
    )

    match user.lang:
        case "RU":
            await callback.message.edit_text(
                text=f"<em>🎁 Ваша реферальная ссылка</em>: <code><b>{user.self_ref_url}</b></code>" + \
                    f"\n\nЗа каждое использование ваш баланс будет пополняться на <b>10 RUB</b> 📈",
                reply_markup=get_back_keyboard()
            )

        case "ENG":
            await callback.message.edit_text(
                text=f"<em>🎁 Your referal link</em>: <code><b>{user.self_ref_url}</b></code>" + \
                    f"\n\nFor each use, your balance will be replenished by <b>10 RUB</b> 📈",
                reply_markup=eng_get_back_keyboard()
            )


@callback_router.callback_query(F.data.startswith("accept_"))
async def accept(callback: CallbackQuery):
    user_id = callback.data.split("_")[1]

    user: User = User.get(
        telegram_id=user_id 
    )

    user.subscribe_status = 1
    user.wait_check = 0
    user.save()

    match user.lang:
        case "RU":
            await callback.bot.send_message(
                chat_id=user_id,
                text="<em>Ваш платеж <b>одобрен</b></em> ✅"
            )

        case "ENG":
            await callback.bot.send_message(
                chat_id=user_id,
                text="<em>Your payment was <b>accepted</b></em> ✅"
            )

    await callback.message.reply(
        "Accepted ✅"
    )


@callback_router.callback_query(F.data.startswith("reject_"))
async def reject(callback: CallbackQuery):
    user_id = callback.data.split("_")[1]

    user: User = User.get(
        telegram_id=user_id 
    )

    user.wait_check = 0
    user.subscribe_status = 0
    user.save()

    match user.lang:
        case "RU":
            await callback.bot.send_message(
                chat_id=user_id,
                text="<em>Ваш платеж <b>отклонен</b></em> ❌"
            )

        case "ENG":
            await callback.bot.send_message(
                chat_id=user_id,
                text="<em>Your payment was <b>rejected</b></em> ❌"
            )

    await callback.message.reply(
        "Rejected ❌"
    )