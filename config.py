"""Loyiha konfiguratsiyasi (.env faylidan o'qiladi)."""
from __future__ import annotations

import base64
import os
import re
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _repair_netscape_cookies(raw: str) -> str:
    """Ba'zi platformalar (Railway, Heroku) env variable'dagi TAB belgilarini
    bo'sh joylarga aylantiradi. Netscape cookies fayli TAB bilan ajratilgan
    maydonlarga ega (7 ta maydon qator boshiga qarab). Qatordagi ketma-ket
    bo'sh joylarni TAB'ga qaytaradi.
    """
    fixed_lines: list[str] = []
    for line in raw.splitlines():
        if not line or line.startswith("#"):
            fixed_lines.append(line)
            continue
        if "\t" in line:
            fixed_lines.append(line)
            continue
        # TAB yo'q — ehtimol bo'sh joylarga aylantirilgan. Ketma-ket 1+ bo'sh joyni TAB bilan almashtiramiz.
        repaired = re.sub(r" +", "\t", line)
        fixed_lines.append(repaired)
    return "\n".join(fixed_lines) + "\n"


def _parse_admin_ids(raw: str) -> list[int]:
    ids: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids.append(int(part))
        except ValueError:
            continue
    return ids


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_ids: list[int]
    db_path: Path
    download_dir: Path
    max_file_size_mb: int
    max_forced_channels: int = 10
    instagram_cookies_file: Path | None = None


def load_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        raise RuntimeError(
            "BOT_TOKEN o'rnatilmagan! Iltimos, .env faylida BOT_TOKEN ni @BotFather bergan token bilan almashtiring."
        )

    admins = _parse_admin_ids(os.getenv("ADMIN_IDS", ""))
    if not admins:
        raise RuntimeError(
            "ADMIN_IDS ko'rsatilmagan! .env faylida kamida bitta admin Telegram user ID ni kiriting."
        )

    db_path = BASE_DIR / os.getenv("DB_PATH", "bot.db")
    download_dir = BASE_DIR / os.getenv("DOWNLOAD_DIR", "downloads")
    download_dir.mkdir(parents=True, exist_ok=True)

    try:
        max_mb = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
    except ValueError:
        max_mb = 50

    cookies_path: Path | None = None
    cookies_content: str | None = None

    cookies_b64 = os.getenv("INSTAGRAM_COOKIES_B64", "").strip()
    if cookies_b64:
        try:
            cookies_content = base64.b64decode(cookies_b64).decode("utf-8")
        except Exception:
            cookies_content = None

    if not cookies_content:
        cookies_raw = os.getenv("INSTAGRAM_COOKIES", "").strip()
        if cookies_raw:
            cookies_content = _repair_netscape_cookies(cookies_raw)

    if cookies_content:
        cookies_path = BASE_DIR / ".instagram_cookies.txt"
        cookies_path.write_text(cookies_content, encoding="utf-8")
    else:
        env_path = os.getenv("INSTAGRAM_COOKIES_FILE", "").strip()
        if env_path:
            p = Path(env_path)
            if p.exists():
                cookies_path = p

    return Settings(
        bot_token=token,
        admin_ids=admins,
        db_path=db_path,
        download_dir=download_dir,
        max_file_size_mb=max_mb,
        instagram_cookies_file=cookies_path,
    )
