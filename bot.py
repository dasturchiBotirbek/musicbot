"""Musiqa/video yuklovchi Telegram bot — kirish nuqtasi."""
from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_settings
from database import Database
from handlers import build_root_router


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    settings = load_settings()

    db = Database(settings.db_path)
    await db.init()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Handlerlarga qo'shimcha konteks (DI)
    dp["db"] = db
    dp["settings"] = settings

    dp.include_router(build_root_router())

    me = await bot.get_me()
    logging.info("Bot ishga tushdi: @%s (id=%s)", me.username, me.id)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
