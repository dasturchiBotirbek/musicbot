"""/start, /help, /language va asosiy menyu."""
from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from database import Database
from utils.i18n import DEFAULT_LANG, LANG_NAMES, SUPPORTED_LANGS, t
from utils.subscription import build_subscribe_keyboard, get_unsubscribed_channels

router = Router(name="common")


def main_menu_keyboard(lang: str | None) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("btn_search", lang)), KeyboardButton(text=t("btn_top", lang))],
            [KeyboardButton(text=t("btn_instructions", lang)), KeyboardButton(text=t("btn_help", lang))],
            [KeyboardButton(text=t("btn_language", lang))],
        ],
        resize_keyboard=True,
        input_field_placeholder=t("menu_placeholder", lang),
    )


def language_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=LANG_NAMES[code], callback_data=f"setlang:{code}")]
        for code in SUPPORTED_LANGS
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def get_lang(db: Database, user_id: int) -> str:
    return (await db.get_language(user_id)) or DEFAULT_LANG


async def _require_subscription(message: Message, db: Database, lang: str) -> bool:
    unsub = await get_unsubscribed_channels(message.bot, db, message.from_user.id)
    if unsub:
        await message.answer(
            t("must_subscribe", lang),
            reply_markup=build_subscribe_keyboard(unsub, lang),
        )
        return False
    return True


@router.message(CommandStart())
async def cmd_start(message: Message, db: Database):
    user = message.from_user
    await db.upsert_user(user.id, user.username, user.full_name)
    lang = await db.get_language(user.id)

    # Yangi foydalanuvchi — tilni tanlashni so'raymiz
    if not lang:
        await message.answer(
            t("choose_language", DEFAULT_LANG),
            reply_markup=language_keyboard(),
        )
        return

    if not await _require_subscription(message, db, lang):
        return

    await message.answer(
        t("welcome", lang, name=user.full_name or "user"),
        reply_markup=main_menu_keyboard(lang),
    )


@router.message(Command("language"))
async def cmd_language(message: Message, db: Database):
    lang = await get_lang(db, message.from_user.id)
    await message.answer(t("choose_language", lang), reply_markup=language_keyboard())


@router.message(F.text.in_({"🌐 Til", "🌐 Язык", "🌐 Language"}))
async def btn_language(message: Message, db: Database):
    lang = await get_lang(db, message.from_user.id)
    await message.answer(t("choose_language", lang), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("setlang:"))
async def cb_set_language(cb: CallbackQuery, db: Database):
    code = cb.data.split(":", 1)[1]
    if code not in SUPPORTED_LANGS:
        await cb.answer()
        return
    await db.upsert_user(cb.from_user.id, cb.from_user.username, cb.from_user.full_name)
    await db.set_language(cb.from_user.id, code)
    await cb.message.edit_text(t("language_set", code, lang=LANG_NAMES[code]))
    # Obunani tekshirib, salom xabarini yuborish
    unsub = await get_unsubscribed_channels(cb.bot, db, cb.from_user.id)
    if unsub:
        await cb.message.answer(
            t("must_subscribe", code),
            reply_markup=build_subscribe_keyboard(unsub, code),
        )
    else:
        await cb.message.answer(
            t("welcome", code, name=cb.from_user.full_name or "user"),
            reply_markup=main_menu_keyboard(code),
        )
    await cb.answer()


@router.message(Command("help"))
@router.message(F.text.in_({"ℹ️ Yordam", "ℹ️ Помощь", "ℹ️ Help"}))
async def cmd_help(message: Message, db: Database):
    lang = await get_lang(db, message.from_user.id)
    if not await _require_subscription(message, db, lang):
        return
    await message.answer(t("help", lang), reply_markup=main_menu_keyboard(lang))


@router.message(F.text.in_({"📥 Yuklash yo'riqnomasi", "📥 Инструкция", "📥 How to download"}))
async def cmd_instructions(message: Message, db: Database):
    lang = await get_lang(db, message.from_user.id)
    if not await _require_subscription(message, db, lang):
        return
    await message.answer(t("instructions", lang))


@router.callback_query(F.data == "check_subscription")
async def cb_check_subscription(cb: CallbackQuery, db: Database):
    lang = await get_lang(db, cb.from_user.id)
    unsub = await get_unsubscribed_channels(cb.bot, db, cb.from_user.id)
    if unsub:
        await cb.answer(t("not_all_subscribed", lang), show_alert=True)
        return
    await cb.message.edit_text(t("subscribed_ok", lang))
    await cb.message.answer(
        t("welcome", lang, name=cb.from_user.full_name or "user"),
        reply_markup=main_menu_keyboard(lang),
    )
    await cb.answer()
