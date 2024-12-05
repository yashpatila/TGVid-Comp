import asyncio
import shutil
import humanize
from time import sleep
from config import Config
from script import Txt
from helper.database import db
from pyrogram.errors import FloodWait
from pyrogram import Client, filters, enums
from .check_user_status import handle_user_status
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.private & filters.command('start'))
async def Handle_StartMsg(bot: Client, msg: Message):
    btn = [[InlineKeyboardButton(text='❗ Hᴇʟᴘ', callback_data='help')],
           [InlineKeyboardButton(text='📢 Uᴘᴅᴀᴛᴇs', url='https://t.me/AIORFT')],
           [InlineKeyboardButton(text='💻 Dᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/Snowball_Official')]]

    if Config.START_PIC:
        await msg.reply_photo(photo=Config.START_PIC, 
                              caption=f"Hello {msg.from_user.mention},\nSend me a video and I'll compress it to 720p.",
                              reply_markup=InlineKeyboardMarkup(btn))
    else:
        await msg.reply_text(text=f"Hello {msg.from_user.mention},\nSend me a video and I'll compress it to 720p.",
                             reply_markup=InlineKeyboardMarkup(btn))


@Client.on_message(filters.private & (filters.video | filters.document))
async def Handle_Video(bot: Client, msg: Message):
    # Automatically trigger compression.
    try:
        file = getattr(msg, msg.media.value)
        ffmpeg = "-preset veryfast -c:v libx264 -s 1280x720 -x265-params 'bframes=8:psy-rd=1:ref=3:aq-mode=3:aq-strength=0.8:deblock=1,1' -pix_fmt yuv420p -crf 25 -c:a libopus -b:a 32k -c:s copy -map 0 -ac 2 -ab 32k -vbr 2 -level 3.1 -threads 15"
        c_thumb = await db.get_thumbnail(msg.from_user.id)
        await msg.reply_text("Compressing your video to 720p. Please wait...")
        await CompressVideo(bot=bot, query=msg, ffmpegcode=ffmpeg, c_thumb=c_thumb)
    except Exception as e:
        print(e)
        await msg.reply_text("Failed to compress video.")
