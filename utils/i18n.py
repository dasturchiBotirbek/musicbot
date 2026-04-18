"""Uch tilli tarjimalar (o'zbek / rus / ingliz)."""
from __future__ import annotations

from typing import Any

DEFAULT_LANG = "uz"
SUPPORTED_LANGS = ("uz", "ru", "en")

LANG_NAMES = {
    "uz": "🇺🇿 O'zbekcha",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ---------- Common ----------
    "choose_language": {
        "uz": "🌐 Iltimos, tilni tanlang:",
        "ru": "🌐 Пожалуйста, выберите язык:",
        "en": "🌐 Please choose a language:",
    },
    "language_set": {
        "uz": "✅ Til o'zgartirildi: {lang}",
        "ru": "✅ Язык изменён: {lang}",
        "en": "✅ Language changed: {lang}",
    },
    "welcome": {
        "uz": (
            "👋 Assalomu alaykum, {name}!\n\n"
            "Men <b>musiqa va video yuklovchi</b> botman.\n\n"
            "✅ <b>Imkoniyatlar:</b>\n"
            "• YouTube'dan musiqa (MP3) yuklash\n"
            "• YouTube'dan video yuklash\n"
            "• Instagram videolarini yuklash\n"
            "• Musiqa nomi bo'yicha qidirish\n"
            "• TOP musiqalar ro'yxati\n\n"
            "📎 Link yuboring yoki qo'shiq nomini yozing."
        ),
        "ru": (
            "👋 Здравствуйте, {name}!\n\n"
            "Я бот для <b>скачивания музыки и видео</b>.\n\n"
            "✅ <b>Возможности:</b>\n"
            "• Скачивание музыки (MP3) с YouTube\n"
            "• Скачивание видео с YouTube\n"
            "• Скачивание видео из Instagram\n"
            "• Поиск по названию песни\n"
            "• ТОП песен\n\n"
            "📎 Отправьте ссылку или название песни."
        ),
        "en": (
            "👋 Hello, {name}!\n\n"
            "I'm a <b>music & video downloader</b> bot.\n\n"
            "✅ <b>Features:</b>\n"
            "• Download YouTube music (MP3)\n"
            "• Download YouTube videos\n"
            "• Download Instagram videos\n"
            "• Search by song name\n"
            "• TOP songs list\n\n"
            "📎 Send a link or song name."
        ),
    },
    "help": {
        "uz": (
            "<b>🆘 Yordam</b>\n\n"
            "• <b>YouTube musiqa:</b> havolani yuboring — MP3 qilib qaytaraman.\n"
            "• <b>YouTube video:</b> havolani yuboring va \"🎬 Video\" tugmasini bosing.\n"
            "• <b>Instagram:</b> post/reel havolasini yuboring.\n"
            "• <b>Qidirish:</b> shunchaki qo'shiq/ijrochi nomini yozing.\n\n"
            "⚠️ Telegram Bot API fayl hajmi cheklovi — 50 MB."
        ),
        "ru": (
            "<b>🆘 Помощь</b>\n\n"
            "• <b>YouTube музыка:</b> отправьте ссылку — верну MP3.\n"
            "• <b>YouTube видео:</b> отправьте ссылку и нажмите \"🎬 Видео\".\n"
            "• <b>Instagram:</b> отправьте ссылку на пост/reel.\n"
            "• <b>Поиск:</b> просто напишите название песни/исполнителя.\n\n"
            "⚠️ Лимит Telegram Bot API на размер файла — 50 МБ."
        ),
        "en": (
            "<b>🆘 Help</b>\n\n"
            "• <b>YouTube music:</b> send a link — I'll return MP3.\n"
            "• <b>YouTube video:</b> send a link and tap \"🎬 Video\".\n"
            "• <b>Instagram:</b> send a post/reel link.\n"
            "• <b>Search:</b> just type a song/artist name.\n\n"
            "⚠️ Telegram Bot API file size limit — 50 MB."
        ),
    },
    "instructions": {
        "uz": (
            "📥 <b>Yuklash:</b>\n\n"
            "1) YouTube havolasini yuboring — default MP3 qilib yuklayman.\n"
            "2) Video versiyasi uchun <b>🎬 Video</b> tugmasini bosing.\n"
            "3) Instagram post/reel havolasini yuborsangiz ham yuklab beraman.\n"
            "4) Faqat matn yozsangiz, YouTube'dan qidirib topaman."
        ),
        "ru": (
            "📥 <b>Скачивание:</b>\n\n"
            "1) Отправьте ссылку YouTube — по умолчанию скачаю MP3.\n"
            "2) Для видео нажмите кнопку <b>🎬 Видео</b>.\n"
            "3) Отправьте ссылку на Instagram пост/reel — скачаю видео.\n"
            "4) Если напишете текст — найду на YouTube."
        ),
        "en": (
            "📥 <b>Download:</b>\n\n"
            "1) Send a YouTube link — I'll return MP3 by default.\n"
            "2) For video, tap the <b>🎬 Video</b> button.\n"
            "3) Send an Instagram post/reel link to download video.\n"
            "4) Send plain text to search on YouTube."
        ),
    },

    # ---------- Menu buttons ----------
    "btn_search": {"uz": "🎵 Musiqa qidirish", "ru": "🎵 Поиск музыки", "en": "🎵 Search music"},
    "btn_top": {"uz": "🔥 TOP musiqalar", "ru": "🔥 ТОП песен", "en": "🔥 TOP songs"},
    "btn_instructions": {"uz": "📥 Yuklash yo'riqnomasi", "ru": "📥 Инструкция", "en": "📥 How to download"},
    "btn_help": {"uz": "ℹ️ Yordam", "ru": "ℹ️ Помощь", "en": "ℹ️ Help"},
    "btn_language": {"uz": "🌐 Til", "ru": "🌐 Язык", "en": "🌐 Language"},
    "btn_check_sub": {"uz": "✅ Tekshirish", "ru": "✅ Проверить", "en": "✅ Check"},
    "btn_audio": {"uz": "🎵 Audio (MP3)", "ru": "🎵 Аудио (MP3)", "en": "🎵 Audio (MP3)"},
    "btn_video": {"uz": "🎬 Video", "ru": "🎬 Видео", "en": "🎬 Video"},

    "menu_placeholder": {
        "uz": "Link yuboring yoki tugmani tanlang...",
        "ru": "Отправьте ссылку или нажмите кнопку...",
        "en": "Send a link or pick a button...",
    },

    # ---------- Subscription ----------
    "must_subscribe": {
        "uz": "❗️ Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling va <b>Tekshirish</b> tugmasini bosing:",
        "ru": "❗️ Чтобы пользоваться ботом, подпишитесь на каналы ниже и нажмите <b>Проверить</b>:",
        "en": "❗️ To use the bot, please subscribe to the channels below and tap <b>Check</b>:",
    },
    "not_all_subscribed": {
        "uz": "Siz hali hamma kanallarga obuna bo'lmagansiz.",
        "ru": "Вы ещё не подписаны на все каналы.",
        "en": "You haven't subscribed to all channels yet.",
    },
    "subscribed_ok": {
        "uz": "✅ Obuna tasdiqlandi! Endi botdan foydalanishingiz mumkin.",
        "ru": "✅ Подписка подтверждена! Теперь можно пользоваться ботом.",
        "en": "✅ Subscription confirmed! You can use the bot now.",
    },

    # ---------- Downloads ----------
    "choose_format": {
        "uz": "🤔 Qaysi formatda yuklab berishim kerak?",
        "ru": "🤔 В каком формате скачать?",
        "en": "🤔 Which format should I download?",
    },
    "downloading": {
        "uz": "⏳ Yuklanmoqda... biroz kuting.",
        "ru": "⏳ Загружаю... подождите немного.",
        "en": "⏳ Downloading... please wait.",
    },
    "searching": {
        "uz": "🔎 <i>{query}</i> — qidirilmoqda va yuklanmoqda...",
        "ru": "🔎 <i>{query}</i> — ищу и загружаю...",
        "en": "🔎 <i>{query}</i> — searching and downloading...",
    },
    "send_song_name": {
        "uz": "🔎 Qo'shiq yoki ijrochi nomini yuboring.",
        "ru": "🔎 Отправьте название песни или исполнителя.",
        "en": "🔎 Send a song or artist name.",
    },
    "only_yt_ig": {
        "uz": "❌ Faqat YouTube yoki Instagram havolalari qabul qilinadi.",
        "ru": "❌ Принимаются только ссылки YouTube или Instagram.",
        "en": "❌ Only YouTube or Instagram links are accepted.",
    },
    "size_too_big": {
        "uz": "⚠️ Fayl hajmi {size:.1f} MB — Telegram cheklovi {limit} MB.",
        "ru": "⚠️ Размер файла {size:.1f} МБ — лимит Telegram {limit} МБ.",
        "en": "⚠️ File size {size:.1f} MB — Telegram limit is {limit} MB.",
    },
    "download_error": {
        "uz": "❌ Yuklab bo'lmadi: <code>{err}</code>",
        "ru": "❌ Не удалось скачать: <code>{err}</code>",
        "en": "❌ Download failed: <code>{err}</code>",
    },
    "expired_request": {
        "uz": "⏱ So'rov muddati tugagan. Havolani qayta yuboring.",
        "ru": "⏱ Срок запроса истёк. Отправьте ссылку ещё раз.",
        "en": "⏱ Request expired. Please send the link again.",
    },

    # ---------- Top ----------
    "top_empty": {
        "uz": "🔥 Hozircha TOP musiqalar ro'yxati bo'sh.\nQo'shiq nomini yozing yoki YouTube havolasini yuboring — birinchi TOPni siz to'ldirasiz! 🎶",
        "ru": "🔥 Пока ТОП песен пуст.\nНапишите название песни или отправьте ссылку YouTube — и заполните ТОП первым! 🎶",
        "en": "🔥 TOP songs list is empty for now.\nType a song name or send a YouTube link — be the first to fill the TOP! 🎶",
    },
    "top_header": {
        "uz": "🔥 <b>TOP 10 musiqalar</b>\n",
        "ru": "🔥 <b>ТОП 10 песен</b>\n",
        "en": "🔥 <b>TOP 10 songs</b>\n",
    },
    "top_row_count": {
        "uz": "{marta} marta",
        "ru": "{marta} раз",
        "en": "{marta} times",
    },

    # ---------- Admin ----------
    "not_admin": {"uz": "⛔️ Siz admin emassiz.", "ru": "⛔️ Вы не админ.", "en": "⛔️ You are not an admin."},
    "admin_panel": {"uz": "🛠 <b>Admin panel</b>", "ru": "🛠 <b>Админ-панель</b>", "en": "🛠 <b>Admin panel</b>"},
    "admin_closed": {"uz": "Admin panel yopildi.", "ru": "Админ-панель закрыта.", "en": "Admin panel closed."},
    "adm_stats": {"uz": "📊 Statistika", "ru": "📊 Статистика", "en": "📊 Stats"},
    "adm_channels": {"uz": "📢 Kanallar", "ru": "📢 Каналы", "en": "📢 Channels"},
    "adm_addchannel": {"uz": "➕ Kanal qo'shish", "ru": "➕ Добавить канал", "en": "➕ Add channel"},
    "adm_broadcast": {"uz": "📨 Broadcast (xabar yuborish)", "ru": "📨 Рассылка", "en": "📨 Broadcast"},
    "adm_top": {"uz": "🔥 TOP musiqalar", "ru": "🔥 ТОП песен", "en": "🔥 TOP songs"},
    "adm_close": {"uz": "❌ Yopish", "ru": "❌ Закрыть", "en": "❌ Close"},
    "adm_back": {"uz": "⬅️ Orqaga", "ru": "⬅️ Назад", "en": "⬅️ Back"},
    "stats_text": {
        "uz": "📊 <b>Statistika</b>\n\n👤 Foydalanuvchilar: <b>{users}</b>\n📥 Jami yuklashlar: <b>{downloads}</b>\n📢 Majburiy kanallar: <b>{channels}</b> / {max_channels}",
        "ru": "📊 <b>Статистика</b>\n\n👤 Пользователи: <b>{users}</b>\n📥 Всего загрузок: <b>{downloads}</b>\n📢 Обязательные каналы: <b>{channels}</b> / {max_channels}",
        "en": "📊 <b>Stats</b>\n\n👤 Users: <b>{users}</b>\n📥 Total downloads: <b>{downloads}</b>\n📢 Required channels: <b>{channels}</b> / {max_channels}",
    },
    "channels_empty": {
        "uz": "📢 Hali birorta majburiy kanal qo'shilmagan.",
        "ru": "📢 Ни одного обязательного канала пока не добавлено.",
        "en": "📢 No required channels added yet.",
    },
    "channels_list_header": {
        "uz": "📢 <b>Majburiy kanallar</b> ({count}/{max_count})\n",
        "ru": "📢 <b>Обязательные каналы</b> ({count}/{max_count})\n",
        "en": "📢 <b>Required channels</b> ({count}/{max_count})\n",
    },
    "channel_deleted": {"uz": "🗑 O'chirildi", "ru": "🗑 Удалено", "en": "🗑 Deleted"},
    "channel_not_found": {"uz": "Topilmadi", "ru": "Не найдено", "en": "Not found"},
    "channels_limit": {
        "uz": "Maksimal {max_count} ta kanal qo'shish mumkin.",
        "ru": "Максимум {max_count} каналов.",
        "en": "Maximum of {max_count} channels allowed.",
    },
    "add_channel_hint": {
        "uz": "➕ Kanal qo'shish uchun quyidagilardan birini yuboring:\n\n• Kanal <b>@username</b> (public kanal)\n• Kanalning <b>chat_id</b> (masalan, <code>-1001234567890</code>)\n• Kanaldan forward qilingan xabar\n\n<i>Muhim: bot kanalda admin bo'lishi shart!</i>\n\nBekor qilish: /cancel",
        "ru": "➕ Чтобы добавить канал, отправьте:\n\n• <b>@username</b> канала (публичный)\n• <b>chat_id</b> канала (например, <code>-1001234567890</code>)\n• пересланное сообщение из канала\n\n<i>Важно: бот должен быть админом в канале!</i>\n\nОтмена: /cancel",
        "en": "➕ To add a channel, send one of:\n\n• Channel <b>@username</b> (public)\n• Channel <b>chat_id</b> (e.g. <code>-1001234567890</code>)\n• A forwarded message from the channel\n\n<i>Important: bot must be admin in the channel!</i>\n\nCancel: /cancel",
    },
    "cancelled": {"uz": "❌ Bekor qilindi.", "ru": "❌ Отменено.", "en": "❌ Cancelled."},
    "send_channel_ref": {
        "uz": "❌ Iltimos, @username, chat_id yoki forward yuboring.",
        "ru": "❌ Отправьте @username, chat_id или пересланное сообщение.",
        "en": "❌ Please send @username, chat_id, or a forward.",
    },
    "channel_not_accessible": {
        "uz": "❌ Kanalni topib bo'lmadi: <code>{err}</code>\n\nBotni kanalga admin sifatida qo'shganingizga ishonch hosil qiling.",
        "ru": "❌ Канал не найден: <code>{err}</code>\n\nУбедитесь, что бот добавлен в канал как админ.",
        "en": "❌ Channel not found: <code>{err}</code>\n\nMake sure the bot is added as admin in the channel.",
    },
    "bot_not_admin": {
        "uz": "⚠️ Bot kanalda admin emas. Iltimos, botni kanalga admin qilib qo'shing va qayta urinib ko'ring.",
        "ru": "⚠️ Бот не админ в канале. Добавьте бота как админа и попробуйте снова.",
        "en": "⚠️ Bot is not admin in the channel. Add the bot as admin and try again.",
    },
    "check_error": {
        "uz": "⚠️ Tekshirishda xatolik: <code>{err}</code>",
        "ru": "⚠️ Ошибка проверки: <code>{err}</code>",
        "en": "⚠️ Check error: <code>{err}</code>",
    },
    "channel_added": {
        "uz": "✅ <b>{title}</b> majburiy kanallar ro'yxatiga qo'shildi.",
        "ru": "✅ <b>{title}</b> добавлен в список обязательных каналов.",
        "en": "✅ <b>{title}</b> added to required channels.",
    },
    "broadcast_hint": {
        "uz": "📨 Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yuboring (har qanday turdagi xabar).\n\nBekor qilish: /cancel",
        "ru": "📨 Отправьте сообщение, которое хотите разослать всем пользователям (любой тип).\n\nОтмена: /cancel",
        "en": "📨 Send the message you want to broadcast to all users (any type).\n\nCancel: /cancel",
    },
    "broadcast_progress": {
        "uz": "📨 Yuborilmoqda... ({i}/{total})",
        "ru": "📨 Отправка... ({i}/{total})",
        "en": "📨 Sending... ({i}/{total})",
    },
    "broadcast_done": {
        "uz": "✅ Broadcast yakunlandi.\n\nYuborildi: <b>{sent}</b>\nYuborilmadi: <b>{failed}</b>",
        "ru": "✅ Рассылка завершена.\n\nОтправлено: <b>{sent}</b>\nНе отправлено: <b>{failed}</b>",
        "en": "✅ Broadcast done.\n\nSent: <b>{sent}</b>\nFailed: <b>{failed}</b>",
    },
    "no_downloads_yet": {
        "uz": "🔥 Hali yuklashlar yo'q.",
        "ru": "🔥 Загрузок пока нет.",
        "en": "🔥 No downloads yet.",
    },
    "search_usage": {
        "uz": "🔎 Foydalanish: <code>/search qo'shiq nomi</code>",
        "ru": "🔎 Использование: <code>/search название песни</code>",
        "en": "🔎 Usage: <code>/search song name</code>",
    },
}


def t(key: str, lang: str | None, **kwargs: Any) -> str:
    lang = lang if lang in SUPPORTED_LANGS else DEFAULT_LANG
    entry = TRANSLATIONS.get(key)
    if not entry:
        return key
    text = entry.get(lang) or entry.get(DEFAULT_LANG) or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text
