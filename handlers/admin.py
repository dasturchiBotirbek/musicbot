"""Admin panel: kanallarni boshqarish, statistika, broadcast."""
from __future__ import annotations

import asyncio
import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import Settings
from database import Database
from utils.i18n import DEFAULT_LANG, t

logger = logging.getLogger(__name__)
router = Router(name="admin")


class AdminStates(StatesGroup):
    waiting_channel = State()
    waiting_broadcast = State()


def _is_admin(user_id: int, settings: Settings) -> bool:
    return user_id in settings.admin_ids


async def _lang(db: Database, user_id: int) -> str:
    return (await db.get_language(user_id)) or DEFAULT_LANG


def _admin_menu(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("adm_stats", lang), callback_data="adm:stats")],
            [InlineKeyboardButton(text=t("adm_channels", lang), callback_data="adm:channels")],
            [InlineKeyboardButton(text=t("adm_addchannel", lang), callback_data="adm:addchannel")],
            [InlineKeyboardButton(text=t("adm_broadcast", lang), callback_data="adm:broadcast")],
            [InlineKeyboardButton(text=t("adm_top", lang), callback_data="adm:top")],
            [InlineKeyboardButton(text=t("adm_close", lang), callback_data="adm:close")],
        ]
    )


def _channels_kb(channels: list[dict], lang: str) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for ch in channels:
        title = ch.get("title") or ch["chat_id"]
        rows.append(
            [
                InlineKeyboardButton(text=f"📢 {title}", callback_data=f"adm:chinfo:{ch['id']}"),
                InlineKeyboardButton(text="🗑", callback_data=f"adm:chdel:{ch['id']}"),
            ]
        )
    rows.append([InlineKeyboardButton(text=t("adm_addchannel", lang), callback_data="adm:addchannel")])
    rows.append([InlineKeyboardButton(text=t("adm_back", lang), callback_data="adm:menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


@router.message(Command("admin"))
async def cmd_admin(message: Message, settings: Settings, db: Database):
    lang = await _lang(db, message.from_user.id)
    if not _is_admin(message.from_user.id, settings):
        await message.answer(t("not_admin", lang))
        return
    await message.answer(t("admin_panel", lang), reply_markup=_admin_menu(lang))


@router.callback_query(F.data == "adm:menu")
async def cb_menu(cb: CallbackQuery, settings: Settings, db: Database):
    lang = await _lang(db, cb.from_user.id)
    if not _is_admin(cb.from_user.id, settings):
        await cb.answer(t("not_admin", lang), show_alert=True)
        return
    await cb.message.edit_text(t("admin_panel", lang), reply_markup=_admin_menu(lang))
    await cb.answer()


@router.callback_query(F.data == "adm:close")
async def cb_close(cb: CallbackQuery, settings: Settings, db: Database):
    if not _is_admin(cb.from_user.id, settings):
        return
    lang = await _lang(db, cb.from_user.id)
    await cb.message.edit_text(t("admin_closed", lang))
    await cb.answer()


@router.callback_query(F.data == "adm:stats")
async def cb_stats(cb: CallbackQuery, db: Database, settings: Settings):
    lang = await _lang(db, cb.from_user.id)
    if not _is_admin(cb.from_user.id, settings):
        await cb.answer(t("not_admin", lang), show_alert=True)
        return
    users = await db.user_count()
    downloads = await db.download_count()
    channels = await db.channel_count()
    text = t(
        "stats_text",
        lang,
        users=users,
        downloads=downloads,
        channels=channels,
        max_channels=settings.max_forced_channels,
    )
    await cb.message.edit_text(text, reply_markup=_admin_menu(lang))
    await cb.answer()


@router.callback_query(F.data == "adm:channels")
async def cb_channels(cb: CallbackQuery, db: Database, settings: Settings):
    lang = await _lang(db, cb.from_user.id)
    if not _is_admin(cb.from_user.id, settings):
        await cb.answer(t("not_admin", lang), show_alert=True)
        return
    channels = await db.list_channels()
    if not channels:
        await cb.message.edit_text(t("channels_empty", lang), reply_markup=_channels_kb([], lang))
    else:
        header = t("channels_list_header", lang, count=len(channels), max_count=settings.max_forced_channels)
        body = "\n".join(
            f"{i+1}. {ch.get('title') or ch['chat_id']}  —  <code>{ch['chat_id']}</code>"
            for i, ch in enumerate(channels)
        )
        await cb.message.edit_text(header + "\n" + body, reply_markup=_channels_kb(channels, lang))
    await cb.answer()


@router.callback_query(F.data.startswith("adm:chdel:"))
async def cb_channel_delete(cb: CallbackQuery, db: Database, settings: Settings):
    lang = await _lang(db, cb.from_user.id)
    if not _is_admin(cb.from_user.id, settings):
        await cb.answer(t("not_admin", lang), show_alert=True)
        return
    try:
        channel_id = int(cb.data.split(":")[2])
    except (IndexError, ValueError):
        await cb.answer()
        return
    ok = await db.remove_channel(channel_id)
    await cb.answer(t("channel_deleted" if ok else "channel_not_found", lang))
    await cb_channels(cb, db, settings)


@router.callback_query(F.data == "adm:addchannel")
async def cb_addchannel(cb: CallbackQuery, db: Database, settings: Settings, state: FSMContext):
    lang = await _lang(db, cb.from_user.id)
    if not _is_admin(cb.from_user.id, settings):
        await cb.answer(t("not_admin", lang), show_alert=True)
        return
    if await db.channel_count() >= settings.max_forced_channels:
        await cb.answer(t("channels_limit", lang, max_count=settings.max_forced_channels), show_alert=True)
        return
    await state.set_state(AdminStates.waiting_channel)
    await cb.message.answer(t("add_channel_hint", lang))
    await cb.answer()


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext, settings: Settings, db: Database):
    if not _is_admin(message.from_user.id, settings):
        return
    lang = await _lang(db, message.from_user.id)
    await state.clear()
    await message.answer(t("cancelled", lang), reply_markup=_admin_menu(lang))


@router.message(AdminStates.waiting_channel)
async def msg_add_channel(message: Message, state: FSMContext, db: Database, settings: Settings):
    if not _is_admin(message.from_user.id, settings):
        return
    lang = await _lang(db, message.from_user.id)
    if await db.channel_count() >= settings.max_forced_channels:
        await state.clear()
        await message.answer(t("channels_limit", lang, max_count=settings.max_forced_channels))
        return

    chat_id: str | None = None
    if message.forward_from_chat:
        chat_id = str(message.forward_from_chat.id)
    elif message.text:
        chat_id = message.text.strip()

    if not chat_id:
        await message.answer(t("send_channel_ref", lang))
        return

    try:
        chat = await message.bot.get_chat(chat_id)
    except TelegramAPIError as exc:
        await message.answer(t("channel_not_accessible", lang, err=str(exc)[:200]))
        return

    try:
        me = await message.bot.get_me()
        member = await message.bot.get_chat_member(chat.id, me.id)
        if member.status not in {"administrator", "creator"}:
            await message.answer(t("bot_not_admin", lang))
            return
    except TelegramAPIError as exc:
        await message.answer(t("check_error", lang, err=str(exc)[:200]))
        return

    invite_url = None
    if chat.username:
        invite_url = f"https://t.me/{chat.username}"
    elif getattr(chat, "invite_link", None):
        invite_url = chat.invite_link
    else:
        try:
            invite = await message.bot.create_chat_invite_link(chat.id)
            invite_url = invite.invite_link
        except TelegramAPIError:
            invite_url = None

    await db.add_channel(str(chat.id), chat.title, invite_url)
    await state.clear()
    await message.answer(t("channel_added", lang, title=chat.title), reply_markup=_admin_menu(lang))


@router.callback_query(F.data == "adm:broadcast")
async def cb_broadcast(cb: CallbackQuery, settings: Settings, state: FSMContext, db: Database):
    lang = await _lang(db, cb.from_user.id)
    if not _is_admin(cb.from_user.id, settings):
        await cb.answer(t("not_admin", lang), show_alert=True)
        return
    await state.set_state(AdminStates.waiting_broadcast)
    await cb.message.answer(t("broadcast_hint", lang))
    await cb.answer()


@router.message(AdminStates.waiting_broadcast)
async def msg_broadcast(message: Message, state: FSMContext, db: Database, settings: Settings):
    if not _is_admin(message.from_user.id, settings):
        return
    lang = await _lang(db, message.from_user.id)
    await state.clear()
    user_ids = await db.all_user_ids()
    status = await message.answer(t("broadcast_progress", lang, i=0, total=len(user_ids)))
    sent = 0
    failed = 0
    for idx, uid in enumerate(user_ids, start=1):
        try:
            await message.copy_to(uid)
            sent += 1
        except TelegramAPIError:
            failed += 1
        if idx % 25 == 0:
            try:
                await status.edit_text(t("broadcast_progress", lang, i=idx, total=len(user_ids)))
            except TelegramAPIError:
                pass
            await asyncio.sleep(1)
    await status.edit_text(t("broadcast_done", lang, sent=sent, failed=failed))


@router.callback_query(F.data == "adm:top")
async def cb_admin_top(cb: CallbackQuery, db: Database, settings: Settings):
    lang = await _lang(db, cb.from_user.id)
    if not _is_admin(cb.from_user.id, settings):
        await cb.answer(t("not_admin", lang), show_alert=True)
        return
    top = await db.top_music(limit=10)
    if not top:
        text = t("no_downloads_yet", lang)
    else:
        lines = [t("top_header", lang)]
        for i, (title, cnt) in enumerate(top, start=1):
            lines.append(f"{i}. {title} — {cnt}")
        text = "\n".join(lines)
    await cb.message.edit_text(text, reply_markup=_admin_menu(lang))
    await cb.answer()


@router.callback_query(F.data.startswith("adm:chinfo:"))
async def cb_chinfo(cb: CallbackQuery, db: Database, settings: Settings):
    lang = await _lang(db, cb.from_user.id)
    if not _is_admin(cb.from_user.id, settings):
        await cb.answer(t("not_admin", lang), show_alert=True)
        return
    try:
        channel_id = int(cb.data.split(":")[2])
    except (IndexError, ValueError):
        await cb.answer()
        return
    channels = await db.list_channels()
    ch = next((c for c in channels if c["id"] == channel_id), None)
    if not ch:
        await cb.answer(t("channel_not_found", lang), show_alert=True)
        return
    text = (
        f"📢 <b>{ch.get('title') or '—'}</b>\n"
        f"chat_id: <code>{ch['chat_id']}</code>\n"
        f"invite: {ch.get('invite_url') or '—'}\n"
        f"added: {ch.get('added_at') or '—'}"
    )
    await cb.answer(text, show_alert=True)
