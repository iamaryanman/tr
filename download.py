import os
import time
import asyncio
import requests
import logging
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def download_video(url, reply_msg, user_mention, user_id):
    response = requests.get(f"https://wooden-adrianna-teraboxapi-c13c449a.koyeb.app/?url={url}")
    response.raise_for_status()
    data = response.json()

    resolutions = data["response"][0]["resolutions"]
    fast_download_link = resolutions["Fast Download"]
    hd_download_link = resolutions["HD Video"]
    thumbnail_url = data["response"][0]["thumbnail"]
    video_title = data["response"][0]["title"]

    try:
        download = aria2.add_uris([fast_download_link])
        start_time = datetime.now()

        while not download.is_complete:
            download.update()
            percentage = download.progress
            done = download.completed_length
            total_size = download.total_length
            speed = download.download_speed
            eta = download.eta
            elapsed_time_seconds = (datetime.now() - start_time).total_seconds()
            progress_text = format_progress_bar(
                filename=video_title,
                percentage=percentage,
                done=done,
                total_size=total_size,
                status=f"Downloading {'🪙' * (percentage // 10)}{'🧲' if percentage == 100 else ''}",
                eta=eta,
                speed=speed,
                elapsed=elapsed_time_seconds,
                user_mention=user_mention,
                user_id=user_id,
                aria2p_gid=download.gid
            )
            await reply_msg.edit_text(progress_text)
            await asyncio.sleep(2)

        if download.is_complete:
            file_path = download.files[0].path

            thumbnail_path = "thumbnail.jpg"
            thumbnail_response = requests.get(thumbnail_url)
            with open(thumbnail_path, "wb") as thumb_file:
                thumb_file.write(thumbnail_response.content)

            await reply_msg.edit_text("ᴜᴘʟᴏᴀᴅɪɴɢ...")

            return file_path, thumbnail_path, video_title
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        buttons = [
            [InlineKeyboardButton("🚀 HD Video", url=hd_download_link)],
            [InlineKeyboardButton("⚡ Fast Download", url=fast_download_link)]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await reply_msg.reply_text(
            "Fast Download Link For this Video is Broken, Download manually using the Link Below.",
            reply_markup=reply_markup
        )
        return None, None, None
