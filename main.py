import os
import config
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database import total_user, getid, delete 

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
    await message.reply_photo(
        photo=config.START_IMG,
        text=config.START_TEXT,
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )

# ==========================[ send After 2 Hr ]=============================== # 

# Function to send image with custom message and inline button

# Function to send broadcast message
async def send_broadcast_message():
    message = "Hello, this is a broadcast message!"
    users = await Bot.get_users(user_ids)
    for user in users:
        await Bot.send_photo(
            user.id,
            photo=config.REPEAT_IMG,
            text=config.REPEAT_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Join Now 🔥", url=f"https://t.me/+oMv-bxaGMXVkNmE0")]])
    )

# Schedule the broadcast every 2 hours
async def broadcast_scheduler():
    while True:
        await send_broadcast_message()
        await asyncio.sleep(300)  # 2 hours in seconds

# Start the broadcast scheduler
with Bot:
    asyncio.get_event_loop().run_until_complete(broadcast_scheduler())
# async def send_image_message(chat_id):
#     await Bot.send_photo(
#         chat_id=message.chat_id,
#         photo=config.REPEAT_IMG,
#         caption=config.REPEAT_TXT,
#         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Join Now 🔥", url=f"https://t.me/+oMv-bxaGMXVkNmE0")]])
#     )

# # Timer to send image message every 2 hours
# while True:
#     time.sleep(300)  # 2 hours = 7200 seconds
#     send_image_message(chat_id)

        
# ==========================[ Bot Run ]=============================== # 

Bot.run()
