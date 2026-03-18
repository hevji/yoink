#!/usr/bin/env python3
"""
Yoink - YouTube Downloader CLI
Usage: yoink <url> [--audio] [--folder <path>]
"""

import sys
import os
import json
import subprocess
import argparse
import re
import shutil
from pathlib import Path

CONFIG_PATH = Path(r"C:\Yoink\config.json")
YOINK_DIR = Path(r"C:\Yoink")

COMMON_FOLDERS = {
    "1": Path.home() / "Downloads",
    "2": Path.home() / "Videos",
    "3": Path.home() / "Music",
    "4": Path(r"C:\Yoink\Downloads"),
}

BANNER = r"""
   :::   :::  :::::::: ::::::::::: ::::    ::: :::    ::: 
  :+:   :+: :+:    :+:    :+:     :+:+:   :+: :+:   :+:   
  +:+ +:+  +:+    +:+    +:+     :+:+:+  +:+ +:+  +:+     
  +#++:   +#+    +:+    +#+     +#+ +:+ +#+ +#++:++       
  +#+    +#+    +#+    +#+     +#+  +#+#+# +#+  +#+       
 #+#    #+#    #+#    #+#     #+#   #+#+# #+#   #+#       
###     ######## ########### ###    #### ###    ###                                           
  Downloading videos made easier.
"""


def print_banner():
    print(BANNER)


def load_config():
    """Load config from disk, return empty dict if missing/corrupt."""
    try:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def save_config(config: dict):
    """Persist config to disk."""
    try:
        YOINK_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        print(f"  [!] Warning: could not save config: {e}")


def check_ffmpeg():
    """Warn user if ffmpeg is not on PATH."""
    if shutil.which("ffmpeg") is None:
        print("  [!] Warning: ffmpeg not found on PATH.")
        print("      High-quality video merging and audio conversion may fail.")
        print("      Download ffmpeg from https://ffmpeg.org/download.html")
        print()


def check_yt_dlp():
    """Ensure yt-dlp is importable; attempt pip install if not."""
    try:
        import yt_dlp  # noqa: F401
        return True
    except ImportError:
        print("  [~] yt-dlp not found. Attempting to install via pip...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "yt-dlp", "--quiet"],
            capture_output=True,
        )
        if result.returncode == 0:
            print("  [+] yt-dlp installed successfully!\n")
            return True
        else:
            print("  [!] Failed to install yt-dlp automatically.")
            print("      Please run: pip install yt-dlp")
            return False


def is_valid_url(url: str) -> bool:
    """Basic URL sanity check."""
    pattern = re.compile(
        r"^(https?://)?"
        r"((www\.)?(youtube\.com|youtu\.be|music\.youtube\.com)"
        r"|[a-zA-Z0-9\-]+\.[a-zA-Z]{2,})"
    )
    return bool(pattern.match(url))


def pick_folder(config: dict) -> Path:
    """
    Return the download folder.
    Uses saved default if present; otherwise prompts the user.
    """
    if "default_folder" in config:
        folder = Path(config["default_folder"])
        print(f"  [>] Using saved folder: {folder}")
        return folder

    print("\n  Where do you want to save downloads?\n")
    for key, path in COMMON_FOLDERS.items():
        print(f"    [{key}] {path}")
    print("    [5] Enter a custom path")
    print()

    while True:
        choice = input("  Choose (1-5): ").strip()
        if choice in COMMON_FOLDERS:
            folder = COMMON_FOLDERS[choice]
            break
        elif choice == "5":
            raw = input("  Enter full path: ").strip().strip('"')
            folder = Path(raw)
            break
        else:
            print("  [!] Invalid choice. Try again.")

    # Offer to save as default
    save_default = input("\n  Save this as your default folder? (y/n): ").strip().lower()
    if save_default == "y":
        config["default_folder"] = str(folder)
        save_config(config)
        print("  [+] Default saved to config.")

    return folder


def is_playlist(url: str) -> bool:
    """Detect playlist URLs."""
    return "playlist" in url.lower() or "list=" in url.lower()


def confirm_playlist():
    """Ask before downloading a whole playlist."""
    print("\n  [?] This looks like a YouTube playlist.")
    answer = input("  Download the entire playlist? (y/n): ").strip().lower()
    return answer == "y"


def build_ydl_opts(folder: Path, audio_only: bool) -> dict:
    """Build yt-dlp options dict."""
    folder.mkdir(parents=True, exist_ok=True)

    if audio_only:
        return {
            "format": "bestaudio/best",
            "outtmpl": str(folder / "%(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "noplaylist": False,
        }
    else:
        return {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": str(folder / "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
            "noplaylist": False,
        }


def download(url: str, folder: Path, audio_only: bool):
    """Run the actual download via yt-dlp."""
    import yt_dlp

    opts = build_ydl_opts(folder, audio_only)
    mode = "audio (MP3)" if audio_only else "video (MP4)"
    print(f"\n  [>] Downloading {mode} to: {folder}\n")

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        print(f"\n  [✓] Done! Saved to: {folder}")
    except yt_dlp.utils.DownloadError as e:
        msg = str(e)
        if "Private video" in msg:
            print("\n  [!] This video is private and cannot be downloaded.")
        elif "This video is not available" in msg or "unavailable" in msg.lower():
            print("\n  [!] This video is unavailable (deleted, region-locked, or removed).")
        elif "Sign in" in msg or "age" in msg.lower():
            print("\n  [!] This video requires sign-in or age verification.")
        elif "Premieres" in msg or "upcoming" in msg.lower():
            print("\n  [!] This video hasn't premiered yet.")
        else:
            print(f"\n  [!] Download failed: {msg}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n  [~] Download cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n  [!] Unexpected error: {e}")
        sys.exit(1)


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        prog="yoink",
        description="Download YouTube videos (or audio) from the command line.",
        add_help=True,
    )
    parser.add_argument("url", nargs="?", help="YouTube URL to download")
    parser.add_argument(
        "--audio", action="store_true", help="Download audio only as MP3"
    )
    parser.add_argument(
        "--folder", type=str, default=None, help="Override download folder"
    )
    parser.add_argument(
        "--reset", action="store_true", help="Reset saved default folder"
    )

    args = parser.parse_args()

    # Handle --reset
    if args.reset:
        config = load_config()
        config.pop("default_folder", None)
        save_config(config)
        print("  [+] Default folder reset. You'll be asked next time.")
        sys.exit(0)

    # Require a URL
    if not args.url:
        print("  Usage: yoink <url> [--audio] [--folder <path>] [--reset]\n")
        print("  Examples:")
        print("    yoink https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("    yoink https://www.youtube.com/watch?v=dQw4w9WgXcQ --audio")
        print("    yoink https://youtube.com/playlist?list=XYZ")
        print("    yoink --reset")
        sys.exit(0)

    url = args.url.strip()

    # Validate URL
    if not is_valid_url(url):
        print(f"  [!] '{url}' doesn't look like a valid URL.")
        print("      Make sure to include https:// or at least a domain name.")
        sys.exit(1)

    # Check dependencies
    if not check_yt_dlp():
        sys.exit(1)
    check_ffmpeg()

    # Playlist check
    if is_playlist(url) and not confirm_playlist():
        print("  [~] Cancelled.")
        sys.exit(0)

    # Determine folder
    config = load_config()
    if args.folder:
        folder = Path(args.folder.strip().strip('"'))
    else:
        folder = pick_folder(config)

    # Download
    download(url, folder, audio_only=args.audio)


if __name__ == "__main__":
    main()
