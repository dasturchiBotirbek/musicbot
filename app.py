"""FastAPI wrapper — botni polling rejimida background task sifatida ishga tushiradi.

Bu wrapper Fly.io kabi platformalarda deploy qilish uchun ishlatiladi — botni tirik ushlab
turish uchun bitta HTTP portini ochib turadi va healthcheck endpoint beradi.
"""
from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI

from config import load_settings
from database import Database
from handlers import build_root_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("musicbot")

_state: dict = {}


async def _run_bot() -> None:
    settings = load_settings()
    db = Database(settings.db_path)
    await db.init()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp["db"] = db
    dp["settings"] = settings
    dp.include_router(build_root_router())

    _state["bot"] = bot
    _state["dp"] = dp

    me = await bot.get_me()
    logger.info("Bot ishga tushdi: @%s (id=%s)", me.username, me.id)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(_run_bot())
    _state["task"] = task
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(title="MusicBot", lifespan=lifespan)


@app.get("/")
async def root():
    bot = _state.get("bot")
    return {
        "status": "ok",
        "bot_running": bot is not None,
        "bot_username": (await bot.get_me()).username if bot else None,
    }


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
