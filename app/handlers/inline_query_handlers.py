import time
from uuid import uuid4

from aiogram import Router, F 
from aiogram.types import InlineQuery, \
    InlineQueryResultArticle, InputTextMessageContent, \
    InlineQueryResult

from app.database.models import Movie


inline_query_router = Router()


@inline_query_router.inline_query(F)
async def movie(inline_query: InlineQuery):
    movies = Movie.select()

    q = inline_query.query[0:-2]
    q.replace(" ", "_")

    result = []
    for i, movie in enumerate(movies):
        if q in movie.tags:
            result.append(InlineQueryResultArticle(
                id=str(uuid4()),
                title=movie.name,
                description=movie.description,
                thumbnail_url=movie.img_url,
                input_message_content=InputTextMessageContent(
                    message_text=movie.name,
                    parse_mode="HTML"
                )
            ))

    await inline_query.answer(results=result)


@inline_query_router.inline_query()
async def movies(inline_query: InlineQuery):
    movies = Movie.select()

    result = []
    for i, movie in enumerate(movies):
        if i <= 49:
            result.append(InlineQueryResultArticle(
                id=str(uuid4()),
                title=movie.name,
                description=movie.description,
                thumbnail_url=movie.img_url,
                input_message_content=InputTextMessageContent(
                    message_text=movie.name,
                    parse_mode="HTML"
                )
            ))
        
        else:
            break

    await inline_query.answer(results=result)