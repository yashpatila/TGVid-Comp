import os
import time
import asyncio
import sys
import humanize
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from helper.utils import Compress_Stats, skip, CompressVideo
from helper.database import db
from script import Txt


@Client.on_callback_query()
async def Cb_Handle(bot: Client, query: CallbackQuery):
    data = query.data

    if data == 'help':
        # No changes here. This block remains as-is.
        btn = [[InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='home')]]
        await query.message.edit(text="This bot automatically compresses videos to 720p.", 
                                 reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)

    elif data == 'home':
        # Home block remains unaltered.
        btn = [[InlineKeyboardButton(text='❗ Hᴇʟᴘ', callback_data='help')],
               [InlineKeyboardButton(text='📢 Uᴘᴅᴀᴛᴇs', url='https://t.me/AIORFT')],
               [InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/Snowball_Official')]]
        await query.message.edit(text=f"Hello {query.from_user.mention}, Welcome back!", 
                                 reply_markup=InlineKeyboardMarkup(btn))

    elif data == 'compress':
        # Auto-trigger compression with 720p settings.
        try:
            file = getattr(query.message.reply_to_message, query.message.reply_to_message.media.value)
            ffmpeg = "-preset veryfast -c:v libx264 -s 1280x720 -x265-params 'bframes=8:psy-rd=1:ref=3:aq-mode=3:aq-strength=0.8:deblock=1,1' -pix_fmt yuv420p -crf 25 -c:a libopus -b:a 32k -c:s copy -map 0 -ac 2 -ab 32k -vbr 2 -level 3.1 -threads 15"
            c_thumb = await db.get_thumbnail(query.from_user.id)
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)
            await query.message.reply_text("Failed to compress video.")

    elif data == "close":
        try:
            await query.message.delete()
        except:
            pass
