# 🎵 Telegram Music & Video Downloader Bot

To'liq ishlaydigan Telegram bot — YouTube'dan **musiqa (MP3)** va **video** yuklab beradi, **Instagram** videolarini saqlaydi, **majburiy obuna** tekshiradi, **admin panel**i bilan boshqariladi va **TOP musiqalar** ro'yxatini ko'rsatadi.

## ✨ Imkoniyatlar

- 🎵 YouTube musiqa (MP3, 192 kbps) yuklash
- 🎬 YouTube video (720p gacha) yuklash
- 📸 Instagram post/reel videolarini yuklash
- 🔎 Qo'shiq nomi bo'yicha qidirib yuklash (YouTube search)
- 🔥 TOP 10 musiqalar ro'yxati (eng ko'p yuklangan)
- 🔐 Majburiy obuna (10 tagacha kanal qo'shsa bo'ladi)
- 🛠 Admin panel:
  - 📊 Statistika (userlar, yuklashlar, kanallar soni)
  - ➕ Kanal qo'shish / 🗑 o'chirish
  - 📨 Broadcast — barcha foydalanuvchilarga xabar yuborish
  - 🔥 TOP musiqalarni ko'rish

## 📦 Talablar

- Python **3.10+**
- **ffmpeg** (MP3 konvertatsiya uchun)

### ffmpeg o'rnatish

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y ffmpeg

# macOS (brew)
brew install ffmpeg

# Windows
# https://www.gyan.dev/ffmpeg/builds/ dan yuklab oling va PATHga qo'shing
```

## 🚀 Ishga tushirish

```bash
# 1) Dependencies
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2) .env faylini sozlang
cp .env.example .env
# .env ichida:
#   BOT_TOKEN=... (@BotFather'dan olasiz)
#   ADMIN_IDS=123456789 (o'zingizning Telegram user ID'ngiz)

# 3) Botni ishga tushirish
python bot.py
```

## ⚙️ .env sozlamalari

| Parametr           | Tavsifi                                                   |
|--------------------|-----------------------------------------------------------|
| `BOT_TOKEN`        | @BotFather bergan bot tokeni                              |
| `ADMIN_IDS`        | Admin Telegram user ID'lari (vergul bilan)                |
| `DB_PATH`          | SQLite fayl nomi                                          |
| `DOWNLOAD_DIR`     | Vaqtincha yuklash papkasi                                 |
| `MAX_FILE_SIZE_MB` | Telegram Bot API cheklovi (default 50)                    |

Telegram user ID ni bilmasangiz — [@userinfobot](https://t.me/userinfobot) ga yozing.

## 🛠 Admin paneldan foydalanish

1. Botga `/admin` deb yozing (ADMIN_IDS ichida bo'lsangiz panel ochiladi).
2. **➕ Kanal qo'shish:**
   - Botni kanalga **admin** qilib qo'shing.
   - Panelda "➕ Kanal qo'shish" ni bosing.
   - Kanal `@username`, `chat_id` yoki forward qilingan xabarni yuboring.
3. **📨 Broadcast:** barcha foydalanuvchilarga matn/rasm/video yuborish.
4. **🗑 Kanalni o'chirish:** kanallar ro'yxatidagi savat belgisini bosing.

## 📁 Loyiha tuzilishi

```
musicbot/
├── bot.py                  # Kirish nuqtasi
├── config.py               # .env yuklash
├── requirements.txt
├── .env.example
├── README.md
├── database/
│   └── db.py               # SQLite (users, channels, downloads)
├── handlers/
│   ├── common.py           # /start, /help, menyu
│   ├── download.py         # YouTube/Instagram yuklash
│   ├── top.py              # TOP musiqalar
│   └── admin.py            # Admin panel
├── services/
│   └── downloader.py       # yt-dlp wrapper
└── utils/
    └── subscription.py     # Majburiy obuna tekshiruvi
```

## ⚠️ Ogohlantirishlar

- Telegram Bot API fayl yuborish cheklovi — **50 MB**. Katta fayllar yuborilmaydi.
- YouTube/Instagram'dan yuklangan kontentdan <b>faqat shaxsiy maqsadlarda</b> foydalaning. Mualliflik huquqlariga rioya qiling.
- Agar Instagram login talab qilsa (yopiq akkauntlar), `cookies.txt` qo'shish kerak bo'lishi mumkin.

## 📝 Litsenziya

MIT
