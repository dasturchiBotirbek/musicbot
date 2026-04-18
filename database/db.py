"""SQLite ma'lumotlar bazasi (aiosqlite orqali)."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import aiosqlite


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id    INTEGER PRIMARY KEY,
    username   TEXT,
    full_name  TEXT,
    language   TEXT DEFAULT 'uz',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS channels (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id    TEXT NOT NULL UNIQUE,
    title      TEXT,
    invite_url TEXT,
    added_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS downloads (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER,
    source      TEXT,          -- youtube_audio / youtube_video / instagram
    title       TEXT,
    url         TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_downloads_title ON downloads(title);
CREATE INDEX IF NOT EXISTS idx_downloads_source ON downloads(source);
"""


class Database:
    def __init__(self, path: Path):
        self.path = path

    async def init(self) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.executescript(SCHEMA)
            # Eski DB'ga language ustuni bo'lmasa, qo'shamiz
            async with db.execute("PRAGMA table_info(users)") as cur:
                cols = [row[1] for row in await cur.fetchall()]
            if "language" not in cols:
                await db.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'uz'")
            await db.commit()

    # ---------- Users ----------
    async def upsert_user(self, user_id: int, username: str | None, full_name: str | None) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                """
                INSERT INTO users (user_id, username, full_name) VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    username=excluded.username,
                    full_name=excluded.full_name
                """,
                (user_id, username, full_name),
            )
            await db.commit()

    async def get_language(self, user_id: int) -> str | None:
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT language FROM users WHERE user_id = ?", (user_id,)) as cur:
                row = await cur.fetchone()
                return row[0] if row and row[0] else None

    async def set_language(self, user_id: int, lang: str) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT INTO users (user_id, language) VALUES (?, ?) "
                "ON CONFLICT(user_id) DO UPDATE SET language=excluded.language",
                (user_id, lang),
            )
            await db.commit()

    async def all_user_ids(self) -> list[int]:
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT user_id FROM users") as cur:
                return [row[0] for row in await cur.fetchall()]

    async def user_count(self) -> int:
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT COUNT(*) FROM users") as cur:
                row = await cur.fetchone()
                return int(row[0]) if row else 0

    # ---------- Channels ----------
    async def list_channels(self) -> list[dict]:
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM channels ORDER BY id") as cur:
                return [dict(r) for r in await cur.fetchall()]

    async def channel_count(self) -> int:
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT COUNT(*) FROM channels") as cur:
                row = await cur.fetchone()
                return int(row[0]) if row else 0

    async def add_channel(self, chat_id: str, title: str | None, invite_url: str | None) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO channels (chat_id, title, invite_url) VALUES (?, ?, ?)",
                (chat_id, title, invite_url),
            )
            await db.commit()

    async def remove_channel(self, channel_id: int) -> bool:
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute("DELETE FROM channels WHERE id = ?", (channel_id,))
            await db.commit()
            return cur.rowcount > 0

    # ---------- Downloads ----------
    async def log_download(self, user_id: int, source: str, title: str | None, url: str | None) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT INTO downloads (user_id, source, title, url) VALUES (?, ?, ?, ?)",
                (user_id, source, title, url),
            )
            await db.commit()

    async def download_count(self) -> int:
        async with aiosqlite.connect(self.path) as db:
            async with db.execute("SELECT COUNT(*) FROM downloads") as cur:
                row = await cur.fetchone()
                return int(row[0]) if row else 0

    async def top_music(self, limit: int = 10) -> list[tuple[str, int]]:
        """Eng ko'p yuklangan musiqalarni qaytaradi."""
        async with aiosqlite.connect(self.path) as db:
            async with db.execute(
                """
                SELECT title, COUNT(*) AS cnt
                FROM downloads
                WHERE source = 'youtube_audio' AND title IS NOT NULL AND title != ''
                GROUP BY title
                ORDER BY cnt DESC
                LIMIT ?
                """,
                (limit,),
            ) as cur:
                return [(row[0], row[1]) for row in await cur.fetchall()]
