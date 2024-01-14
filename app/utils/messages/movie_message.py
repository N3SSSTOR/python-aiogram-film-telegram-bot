from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_file import URLInputFile

from app.database.models import Movie, User


async def send_movie_info(message: Message, movie: Movie):
    user: User = User.get(
        telegram_id=message.from_user.id
    )

    photo = URLInputFile(
        url=movie.img_url,
    )

    if user.subscribe_status:
        await message.answer_photo(
            photo=photo,
            caption=f"<b>{movie.name}</b>" + \
                f"\n\n{movie.description}"
        )

    else:
        match user.lang:
            case "RU":
                await message.answer_photo(
                    photo=photo,
                    caption=f"<b>{movie.name}</b>" + \
                        f"\n\n{movie.description}",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[[
                            InlineKeyboardButton(text="Оформить подписку 👑", callback_data="order_subscribe")
                        ]]
                    )
                )  

            case "ENG":
                await message.answer_photo(
                    photo=photo,
                    caption=f"<b>{movie.name}</b>" + \
                        f"\n\n{movie.description}",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[[
                            InlineKeyboardButton(text="Subscribe 👑", callback_data="order_subscribe")
                        ]]
                    )
                )      