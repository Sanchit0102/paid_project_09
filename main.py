import os
import config
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database import getid, insert, users

# ==========================[ Server Client ]=============================== # 

Bot = Client(
    "Trading Bot",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)

# ==========================[ Start cmd Text ]=============================== # 

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('🔥 Join Now 🔥', url=f'https://t.me/+oMv-bxaGMXVkNmE0')
        ]
    ]
)

@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, message):
    user_id = int(message.from_user.id)
    await insert(user_id)
    await message.reply_photo(
        photo=config.START_IMG,
        text=config.START_TEXT,
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )

# ==========================[ send After 2 Hr ]=============================== # 

# Function to send broadcast message

async def send_broadcast_message():
    # users = await getid(all_users)
    # for user in users:
    
        await Bot.send_photo(
            user_id=database.DS,
            photo=config.REPEAT_IMG,
            text=config.REPEAT_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Join Now 🔥", url=f"https://t.me/+oMv-bxaGMXVkNmE0")]])
         )

async def schedule_broadcast():
    while True:
        await send_broadcast_message()
        await asyncio.sleep(300)  # Sleep for 2 hours (7200 seconds)

# Start the asyncio event loop
asyncio.get_event_loop().run_until_complete(schedule_broadcast())

# ==========================[ Bot Run ]=============================== # 

Bot.run()
