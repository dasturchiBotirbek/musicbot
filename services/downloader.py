"""yt-dlp asosidagi yuklovchi (YouTube va Instagram uchun)."""
from __future__ import annotations

import asyncio
import re
import uuid
from dataclasses import dataclass
from pathlib import Path

import yt_dlp

YOUTUBE_RE = re.compile(r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/", re.IGNORECASE)
INSTAGRAM_RE = re.compile(r"(https?://)?(www\.)?instagram\.com/", re.IGNORECASE)


def is_youtube(url: str) -> bool:
    return bool(YOUTUBE_RE.search(url))


def is_instagram(url: str) -> bool:
    return bool(INSTAGRAM_RE.search(url))


@dataclass
class DownloadResult:
    file_path: Path
    title: str
    duration: int | None
    webpage_url: str | None
    thumbnail: str | None
    uploader: str | None


def _run_ydl(opts: dict, url: str) -> tuple[dict, str]:
    """Sync funksiya — yt-dlp'ni ishga tushiradi va info qaytaradi."""
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if "entries" in info and info["entries"]:
            info = info["entries"][0]
        file_path = ydl.prepare_filename(info)
    return info, file_path


async def _run_in_thread(opts: dict, url: str) -> tuple[dict, str]:
    return await asyncio.to_thread(_run_ydl, opts, url)


def _make_outtmpl(download_dir: Path) -> str:
    unique = uuid.uuid4().hex[:8]
    return str(download_dir / f"%(title).80s-{unique}.%(ext)s")


def _has_ffmpeg() -> bool:
    import shutil
    return shutil.which("ffmpeg") is not None


async def download_youtube_audio(url: str, download_dir: Path) -> DownloadResult:
    outtmpl = _make_outtmpl(download_dir)
    use_ffmpeg = _has_ffmpeg()
    opts: dict
    if use_ffmpeg:
        opts = {
            "format": "bestaudio/best",
            "outtmpl": outtmpl,
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
    else:
        # ffmpeg yo'q — m4a (Telegram audio qo'llab-quvvatlaydi) qilib yuklash
        opts = {
            "format": "bestaudio[ext=m4a]/bestaudio",
            "outtmpl": outtmpl,
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }
    info, file_path = await _run_in_thread(opts, url)
    p = Path(file_path)
    if not p.exists():
        for ext in (".mp3", ".m4a", ".webm", ".opus"):
            candidate = p.with_suffix(ext)
            if candidate.exists():
                p = candidate
                break
    return DownloadResult(
        file_path=p,
        title=info.get("title") or "audio",
        duration=info.get("duration"),
        webpage_url=info.get("webpage_url"),
        thumbnail=info.get("thumbnail"),
        uploader=info.get("uploader") or info.get("channel"),
    )


async def download_youtube_video(url: str, download_dir: Path) -> DownloadResult:
    outtmpl = _make_outtmpl(download_dir)
    use_ffmpeg = _has_ffmpeg()
    # ffmpeg bo'lmasa, merge qila olmaymiz — single-file mp4 format tanlaymiz
    if use_ffmpeg:
        fmt = "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best"
    else:
        fmt = "best[height<=720][ext=mp4]/best[ext=mp4]/best"
    opts = {
        "format": fmt,
        "outtmpl": outtmpl,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
    }
    info, file_path = await _run_in_thread(opts, url)
    p = Path(file_path)
    if not p.exists():
        mp4_candidate = p.with_suffix(".mp4")
        if mp4_candidate.exists():
            p = mp4_candidate
    return DownloadResult(
        file_path=p,
        title=info.get("title") or "video",
        duration=info.get("duration"),
        webpage_url=info.get("webpage_url"),
        thumbnail=info.get("thumbnail"),
        uploader=info.get("uploader") or info.get("channel"),
    )


async def download_instagram(url: str, download_dir: Path) -> DownloadResult:
    outtmpl = _make_outtmpl(download_dir)
    opts = {
        "format": "best",
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
    }
    info, file_path = await _run_in_thread(opts, url)
    p = Path(file_path)
    return DownloadResult(
        file_path=p,
        title=info.get("title") or info.get("description") or "instagram",
        duration=info.get("duration"),
        webpage_url=info.get("webpage_url") or url,
        thumbnail=info.get("thumbnail"),
        uploader=info.get("uploader") or info.get("channel"),
    )


async def search_youtube_audio(query: str, download_dir: Path) -> DownloadResult:
    """Matn bo'yicha YouTube'dan musiqa qidirib yuklash."""
    search_url = f"ytsearch1:{query}"
    return await download_youtube_audio(search_url, download_dir)
