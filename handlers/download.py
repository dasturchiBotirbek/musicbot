"""Musiqa/video yuklash handlerlari."""
from __future__ import annotations

import logging
from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import Settings
from database import Database
from services import downloader
from utils.i18n import DEFAULT_LANG, t
from utils.subscription import build_subscribe_keyboard, get_unsubscribed_channels

logger = logging.getLogger(__name__)

router = Router(name="download")

_PENDING_URLS: dict[str, str] = {}


async def _lang(db: Database, user_id: int) -> str:
    return (await db.get_language(user_id)) or DEFAULT_LANG


def _safe_unlink(path: Path | None) -> None:
    if not path:
        return
    try:
        if path.exists():
            path.unlink()
    except OSError:
        logger.warning("Faylni o'chirib bo'lmadi: %s", path)


def _download_kb(token: str, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_audio", lang), callback_data=f"dl:a:{token}"),
                InlineKeyboardButton(text=t("btn_video", lang), callback_data=f"dl:v:{token}"),
            ]
        ]
    )


async def _ensure_subscribed(message: Message, db: Database, lang: str) -> bool:
    unsub = await get_unsubscribed_channels(message.bot, db, message.from_user.id)
    if unsub:
        await message.answer(t("must_subscribe", lang), reply_markup=build_subscribe_keyboard(unsub, lang))
        return False
    return True


def _check_size(path: Path, settings: Settings) -> bool:
    return path.exists() and path.stat().st_size <= settings.max_file_size_mb * 1024 * 1024


async def _send_audio(message: Message, result: downloader.DownloadResult) -> None:
    file = FSInputFile(result.file_path)
    await message.answer_audio(
        audio=file,
        title=result.title[:60] if result.title else None,
        performer=(result.uploader or "YouTube")[:60],
        duration=int(result.duration or 0),
        caption=f"🎵 <b>{result.title}</b>" if result.title else None,
    )


async def _send_video(message: Message, result: downloader.DownloadResult) -> None:
    file = FSInputFile(result.file_path)
    await message.answer_video(
        video=file,
        caption=f"🎬 <b>{result.title}</b>" if result.title else None,
        duration=int(result.duration or 0),
        supports_streaming=True,
    )


@router.message(Command("search"))
async def cmd_search(message: Message, db: Database, settings: Settings):
    lang = await _lang(db, message.from_user.id)
    if not await _ensure_subscribed(message, db, lang):
        return
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(t("search_usage", lang))
        return
    await _handle_search(message, args[1], db, settings, lang)


async def _handle_search(message: Message, query: str, db: Database, settings: Settings, lang: str) -> None:
    status = await message.answer(t("searching", lang, query=query))
    result: downloader.DownloadResult | None = None
    try:
        result = await downloader.search_youtube_audio(query, settings.download_dir)
        if not _check_size(result.file_path, settings):
            size_mb = result.file_path.stat().st_size / (1024 * 1024) if result.file_path.exists() else 0
            await status.edit_text(t("size_too_big", lang, size=size_mb, limit=settings.max_file_size_mb))
            return
        await _send_audio(message, result)
        await db.log_download(message.from_user.id, "youtube_audio", result.title, result.webpage_url)
        await status.delete()
    except Exception as exc:
        logger.exception("Qidiruvda xato")
        await status.edit_text(t("download_error", lang, err=str(exc)[:200]))
    finally:
        if result:
            _safe_unlink(result.file_path)


@router.message(F.text.in_({"🎵 Musiqa qidirish", "🎵 Поиск музыки", "🎵 Search music"}))
async def btn_search(message: Message, db: Database):
    lang = await _lang(db, message.from_user.id)
    if not await _ensure_subscribed(message, db, lang):
        return
    await message.answer(t("send_song_name", lang))


@router.message(F.text.regexp(r"^https?://\S+"))
async def handle_link(message: Message, db: Database, settings: Settings):
    lang = await _lang(db, message.from_user.id)
    if not await _ensure_subscribed(message, db, lang):
        return
    url = message.text.strip()

    if downloader.is_instagram(url):
        await _download_and_send(message, url, "instagram", db, settings, lang=lang)
        return

    if downloader.is_youtube(url):
        token = f"{message.from_user.id}:{message.message_id}"
        _PENDING_URLS[token] = url
        await message.answer(t("choose_format", lang), reply_markup=_download_kb(token, lang))
        return

    await message.answer(t("only_yt_ig", lang))


@router.callback_query(F.data.startswith("dl:"))
async def cb_download(cb: CallbackQuery, db: Database, settings: Settings):
    lang = await _lang(db, cb.from_user.id)
    parts = cb.data.split(":", 2)
    if len(parts) != 3:
        await cb.answer()
        return
    _, kind, token = parts
    url = _PENDING_URLS.pop(token, None)
    if not url:
        await cb.answer(t("expired_request", lang), show_alert=True)
        try:
            await cb.message.edit_reply_markup(reply_markup=None)
        except Exception:
            pass
        return

    source = "youtube_audio" if kind == "a" else "youtube_video"
    try:
        await cb.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass
    await _download_and_send(cb.message, url, source, db, settings, requested_by=cb.from_user.id, lang=lang)
    await cb.answer()


async def _download_and_send(
    message: Message,
    url: str,
    source: str,
    db: Database,
    settings: Settings,
    requested_by: int | None = None,
    lang: str = DEFAULT_LANG,
) -> None:
    user_id = requested_by or (message.from_user.id if message.from_user else 0)
    status = await message.answer(t("downloading", lang))
    result: downloader.DownloadResult | None = None
    try:
        if source == "youtube_audio":
            result = await downloader.download_youtube_audio(url, settings.download_dir)
        elif source == "youtube_video":
            result = await downloader.download_youtube_video(url, settings.download_dir)
        elif source == "instagram":
            result = await downloader.download_instagram(
                url, settings.download_dir, cookies_file=settings.instagram_cookies_file
            )
        else:
            await status.edit_text(t("download_error", lang, err="unknown source"))
            return

        if not _check_size(result.file_path, settings):
            size_mb = result.file_path.stat().st_size / (1024 * 1024) if result.file_path.exists() else 0
            await status.edit_text(t("size_too_big", lang, size=size_mb, limit=settings.max_file_size_mb))
            return

        if source == "youtube_audio":
            await _send_audio(message, result)
        else:
            await _send_video(message, result)

        await db.log_download(user_id, source, result.title, result.webpage_url or url)
        await status.delete()
    except Exception as exc:
        logger.exception("Yuklashda xato")
        await status.edit_text(t("download_error", lang, err=str(exc)[:200]))
    finally:
        if result:
            _safe_unlink(result.file_path)


@router.message(F.text & ~F.text.startswith("/"))
async def handle_text_as_search(message: Message, db: Database, settings: Settings):
    text = (message.text or "").strip()
    if not text:
        return
    lang = await _lang(db, message.from_user.id)
    if not await _ensure_subscribed(message, db, lang):
        return
    await _handle_search(message, text, db, settings, lang)
