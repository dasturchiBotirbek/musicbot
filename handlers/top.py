"""TOP musiqalar ro'yxati."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from database import Database
from utils.i18n import DEFAULT_LANG, t
from utils.subscription import build_subscribe_keyboard, get_unsubscribed_channels

router = Router(name="top")


async def _lang(db: Database, user_id: int) -> str:
    return (await db.get_language(user_id)) or DEFAULT_LANG


@router.message(Command("top"))
@router.message(F.text.in_({"🔥 TOP musiqalar", "🔥 ТОП песен", "🔥 TOP songs"}))
async def cmd_top(message: Message, db: Database):
    lang = await _lang(db, message.from_user.id)
    unsub = await get_unsubscribed_channels(message.bot, db, message.from_user.id)
    if unsub:
        await message.answer(t("must_subscribe", lang), reply_markup=build_subscribe_keyboard(unsub, lang))
        return

    top = await db.top_music(limit=10)
    if not top:
        await message.answer(t("top_empty", lang))
        return

    lines = [t("top_header", lang)]
    medals = ["🥇", "🥈", "🥉"] + ["🎵"] * 7
    for idx, (title, cnt) in enumerate(top):
        mark = medals[idx] if idx < len(medals) else "🎵"
        lines.append(
            f"{mark} <b>{idx + 1}.</b> {title}  —  <i>{t('top_row_count', lang, marta=cnt)}</i>"
        )
    await message.answer("\n".join(lines))
