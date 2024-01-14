from peewee import DoesNotExist
from datetime import datetime
import time
import asyncio
import os

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command, CommandObject
from aiogram.types import Message, ContentType, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_file import FSInputFile
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import decode_payload, create_start_link
from aiogram.enums.chat_member_status import ChatMemberStatus

from app.database.models import *
from app.utils.captcha.start_captcha import start_captcha
from app.utils.messages.main_menu_message import send_main_menu_message
from app.utils.messages.movie_message import send_movie_info
from app.utils.messages.channel import channel
from app.utils.is_member import is_member
from app.fsm.token_states import TokenStates
from app.fsm.captcha_states import CaptchaStates
from app.fsm.admin_states import AdminStates
from app.keyboards.inline_keyboards import *
from app.keyboards.reply_keyboards import *
from app.middleware.antispam import AntiFloodMiddleware

from config import *



from aiogram import Bot, Dispatcher 
from aiogram.types import BotCommand

from app.handlers.callback_handlers import callback_router
from app.handlers.inline_query_handlers import inline_query_router



message_router = Router() 
message_router.message.middleware(AntiFloodMiddleware())


@message_router.message(TokenStates.token)
async def token(message: Message, state: FSMContext):
    await state.clear()
    
    user: User = User.get(
        telegram_id=message.from_user.id  
    )

    Token.create(
        telegram_token=message.text,
        user_id=user.telegram_id
    )

    match user.lang:
        case "RU":
            await message.answer(
                "Перейдите в @BotFather и введите команду /setinline для своего бота (введите любое значение)"
            )

        case "ENG":
            await message.answer(
                "Go to @BotFather and enter the command /setinline for your bot (enter any value)"
            )

    try:
        # await asyncio.run(
        #     run_user_bot(message.text)
        # )

        bot2 = Bot(
            token=message.text,
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

    except Exception as ex:
        print(ex)
        await message.answer(
            "Telegram Bad Request: Problems with token, bot raised error"
        )


@message_router.message(F.text == "Menu", StateFilter(None))
async def main_menu(message: Message):
    await send_main_menu_message(message=message)


@message_router.message(CommandStart(deep_link=True), StateFilter(None))
async def start_with_ref(message: Message, state: FSMContext, command: CommandObject):
    args = command.args 
    ref_id = args

    try:
        user: User = User.get(
            telegram_id=message.from_user.id
        ) 

    except DoesNotExist:
        self_ref_url = await create_start_link(
            message.bot, 
            str(message.from_user.id), 
            encode=False
        )

        user: User = User.create(
            telegram_id=message.from_user.id,
            date=str(datetime.now().date()),
            self_ref_url=self_ref_url
        )

        user.discount = 3
        user.save()

        ref_user: User = User.get(
            telegram_id=ref_id 
        )

        ref_user.balance = ref_user.balance + 10
        ref_user.save()

        ref_user: User = User.get(
            telegram_id=ref_id 
        )

        match ref_user.lang:
            case "RU":
                await message.bot.send_message(
                    chat_id=ref_user.telegram_id,
                    text=f"🚀 Вы привели нового реферала, баланс: <b>{ref_user.balance} RUB</b>"
                )

            case "ENG":
                await message.bot.send_message(
                    chat_id=ref_user.telegram_id,
                    text=f"🚀 You brought a new referral, balance: <b>{user.balance} RUB</b>"
                )

    # captcha_skip = False
    # channel_skip = False

    # if user.captcha_status == 1:
    #     # await send_main_menu_message(message=message)
    #     captcha_skip = True

    # else:
    #     await start_captcha(message=message)
    #     await state.set_state(CaptchaStates.captcha_text)

    # try:
    #     member = await message.bot.get_chat_member(chat_id=AD_CHANNEL_ID, user_id=message.from_user.id)
    #     channel_skip = True
    #     if member == ChatMemberStatus.LEFT:
    #         channel_skip = False  

    # except:
    #     await channel(message=message)

    # await channel(message=message)

    # if channel_skip and captcha_skip:
    #     await send_main_menu_message(message=message)
    await channel(message=message)
    await start_captcha(message=message)
    await state.set_state(CaptchaStates.captcha_text)


@message_router.message(CommandStart(), StateFilter(None))
async def start(message: Message, state: FSMContext):
    try:
        user: User = User.get(
            telegram_id=message.from_user.id
        ) 

    except DoesNotExist:
        self_ref_url = await create_start_link(
            message.bot, 
            str(message.from_user.id), 
            encode=False
        )

        user: User = User.create(
            telegram_id=message.from_user.id,
            date=str(datetime.now().date()),
            self_ref_url=self_ref_url
        )

    # captcha_skip = False
    # channel_skip = False

    # if user.captcha_status == 1:
    #     # await send_main_menu_message(message=message)
    #     captcha_skip = True

    # else:
    #     await start_captcha(message=message)
    #     await state.set_state(CaptchaStates.captcha_text)

    # try:
    #     member = await message.bot.get_chat_member(chat_id=AD_CHANNEL_ID, user_id=message.from_user.id)
    #     channel_skip = True
    #     if member == ChatMemberStatus.LEFT:
    #         channel_skip = False  

    # except:
    #     await channel(message=message)

    # await channel(message=message)

    # if channel_skip and captcha_skip:
    #     await send_main_menu_message(message=message)
    await channel(message=message)
    await start_captcha(message=message)
    await state.set_state(CaptchaStates.captcha_text)


@message_router.message(CaptchaStates.captcha_text)
async def captcha(message: Message, state: FSMContext):
    user: User = User.get(
        telegram_id=message.from_user.id
    )

    if user.captcha_text == message.text:
        user.captcha_status = 1
        user.last_captcha_time = int(time.time())
        user.captcha_text = None
        user.save()

        match user.lang:
            case "RU":
                await message.answer(
                    "<em>Успешно!</em>",
                    reply_markup=main_reply_keyboard()
                )

            case "ENG":
                await message.answer(
                    "<em>Successfull!</em>",
                )  

        await state.clear()

        await is_member(message=message) 

        user: User = User.get(
            telegram_id=message.from_user.id
        )

        if user.membered:
            await send_main_menu_message(message=message)

        else:
            await channel(message=message)

    else:
        match user.lang:
            case "RU":
                await message.answer(
                    "<em>Данные введены неверно</em>"
                )

            case "ENG":
                await message.answer(
                    "<em>Data entered incorrectly</em>"
                )     

        await start_captcha(message=message)


@message_router.message(F.content_type == ContentType.PHOTO, StateFilter(None))
async def photo(message: Message):
    user: User = User.get(
        telegram_id=message.from_user.id 
    )

    if user.wait_check == 1:
        user.wait_check = 2
        user.save()

        path = f"download/{user.telegram_id}.jpg"

        await message.bot.download(
            file=message.photo[-1].file_id,
            destination=path
        )

        match user.lang:
            case "RU":
                await message.answer(
                    text="<em>Ваш платеж находится на проверке...</em>",
                )   

            case "ENG":
                await message.answer(
                    text="<em>Your payment is being verified...</em>",
                ) 

        debug_photo = FSInputFile(path)
        
        await message.bot.send_photo(
            chat_id=DEBUG_GROUP_ID,
            photo=debug_photo,
            caption=f"User ID: {user.telegram_id}" + \
                f"\nUsername: @{message.from_user.username}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text="✅", callback_data=f"accept_{user.telegram_id}"),
                    InlineKeyboardButton(text="❌", callback_data=f"reject_{user.telegram_id}"),
                ]]
            )
        )


@message_router.message(Command("help"), StateFilter(None))
async def help_message(message: Message):
    user: User = User.get(
        telegram_id=message.from_user.id 
    )

    match user.lang:
        case "RU":
            await message.answer(
                f"📄 <b>Инструкция по использованию бота</b>" + \
                f"\n\n/help -  Инструкция 📄" + \
                f"\n/menu -  Меню 📋" + \
                f"\n\n/find - Найти контент по тегам 🔍 <em>(ниже примеры)</em>" + \
                f"\n/find <em>слово пацана</em> ✅" + \
                f"\n/find <em>Слово пацана. Кровь на асфальте</em> ✅" + \
                f"\n/find <em>найди сериал слово пацана</em> ❌" + \
                f"\n/find <em>слово пацана смотреть</em> ❌"
            )

        case "ENG":
            await message.answer(
                f"📄 <b>Instructions for using the bot</b>" + \
                f"\n\n/help -  Instructions 📄" + \
                f"\n/menu -  Menu 📋" + \
                f"\n\n/find - Find content by tags 🔍 <em>(below are examples)</em>" + \
                f"\n/find <em>breaking bad</em> ✅" + \
                f"\n/find <em>Breaking Bad</em> ✅" + \
                f"\n/find <em>find breaking bad</em> ❌" + \
                f"\n/find <em>breaking bad online free</em> ❌"
            )


@message_router.message(Command("menu"), StateFilter(None))
async def menu(message: Message):
    await send_main_menu_message(message=message)


@message_router.message(F.text == "/send", StateFilter(None))
async def admin_send_command(message: Message, state: FSMContext):
    await state.set_state(AdminStates.send)

    await message.reply(
        "OK. Send your message"
    )


@message_router.message(AdminStates.send)
async def send(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Starting...")

    users = User.select()

    if message.photo and not message.media_group_id:
        if message.caption:
            caption = message.caption

        else:
            caption = ""

        path = f"download/{int(time.time())}.jpg"

        await message.bot.download(
            file=message.photo[-1].file_id,
            destination=path
        )

        photo = FSInputFile(path=path)
            
        for user in users:
            await message.bot.send_photo(
                chat_id=user.telegram_id,
                photo=photo,
                caption=caption
            )

        os.remove(path)

    elif message.photo and message.media_group_id:
        if message.caption:
            caption = message.caption

        else:
            caption = ""

        photos = []
        for photo in message.photo:
            print(message.photo)
            photos.append(InputMediaPhoto(media=photo.file_id))

        for user in users:
            await message.bot.send_media_group(
                chat_id=user.telegram_id, 
                media=photos, 
            )

    else:
        for user in users:
            await message.bot.send_message(
                chat_id=user.telegram_id,
                text=message.text
            )

    await message.answer("OK")
    

@message_router.message(StateFilter(None))
async def find_movie_by_name(message: Message):
    await send_movie_info(
        message=message,
        movie=Movie.get(name=message.text)
    )   