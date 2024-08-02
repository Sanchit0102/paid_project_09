import os
import config
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

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
        text=START_TEXT,
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS
    )

# ==========================[ send After 2 Hr ]=============================== # 

# Function to send image with custom message and inline button

chat_id = message.from_user.id
def send_image_message(chat_id):
    Bot.send_photo(chat_id, photo=config.REPEAT_IMG, caption=config.REPEAT_TXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Join Now 🔥", url=f"https://t.me/+oMv-bxaGMXVkNmE0")]]))

# Timer to send image message every 2 hours
while True:
    time.sleep(300)  # 2 hours = 7200 seconds
    send_image_message(chat_id)

# ==========================[ Bot Run ]=============================== # 

Bot.run()
