"""Majburiy obuna tekshiruvi."""
from __future__ import annotations

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import Database
from utils.i18n import t


async def get_unsubscribed_channels(bot: Bot, db: Database, user_id: int) -> list[dict]:
    """Foydalanuvchi hali obuna bo'lmagan kanallar ro'yxatini qaytaradi."""
    channels = await db.list_channels()
    unsub: list[dict] = []
    for ch in channels:
        try:
            member = await bot.get_chat_member(chat_id=ch["chat_id"], user_id=user_id)
            if member.status in {"left", "kicked"}:
                unsub.append(ch)
        except TelegramAPIError:
            unsub.append(ch)
    return unsub


def build_subscribe_keyboard(channels: list[dict], lang: str | None = None) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for ch in channels:
        url = ch.get("invite_url")
        if not url:
            chat_id = ch["chat_id"]
            if chat_id.startswith("@"):
                url = f"https://t.me/{chat_id[1:]}"
            else:
                continue
        title = ch.get("title") or ch["chat_id"]
        rows.append([InlineKeyboardButton(text=f"📢 {title}", url=url)])
    rows.append([InlineKeyboardButton(text=t("btn_check_sub", lang), callback_data="check_subscription")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
