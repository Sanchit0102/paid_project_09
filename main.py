import os
import config
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database import getid, insert

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

# @Bot.on_message(filters.private & filters.command(["start"]))
# async def start(bot, message):
#     user_id = int(message.from_user.id)
#     await insert(user_id)
#     await message.reply_photo(
#         photo=config.START_IMG,
#         text=config.START_TEXT,
#         disable_web_page_preview=True,
#         reply_markup=START_BUTTONS
#     )

# # ==========================[ send After 2 Hr ]=============================== # 

# # Function to send broadcast message

# async def send_broadcast_message(Bot):
#     users = await Bot.get_user_ids() # getid()
#     user_ids = [user.id for user in users]
#     # for user_id in users:
#     await Bot.send_photo(
#         user_ids,
#         photo=config.REPEAT_IMG,
#         text=config.REPEAT_TXT,
#         disable_web_page_preview=True,
#         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Join Now 🔥", url=f"https://t.me/+oMv-bxaGMXVkNmE0")]])
#     )


# async def schedule_broadcast():
#     while True:
#         await send_broadcast_message(Bot)
#         await asyncio.sleep(300)  # Sleep for 2 hours (7200 seconds)

# # Start the asyncio event loop
# asyncio.get_event_loop().run_until_complete(schedule_broadcast())

# ==========================[ Bot Run ]=============================== # 

Bot.run()




@Bot.on_message(filters.command("start"))
def start_command(client, message):
    # Send a photo with a caption and an inline keyboard button
    photo_url = config.START_IMG
    caption = config.START_TEXT
    reply_markup = START_BUTTONS
    client.send_photo(message.chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup)

# Function to send auto messages every 2 hours to users who started the bot
def send_auto_message():
    while True:
        time.sleep(300)  # 2 hours interval
        users = get_users_to_send_message()  # Implement this function to get users who started the bot
        for user in users:
            BOT.send_message(user, "This is an automated message sent every 2 hours.")

# Start the auto message sender
send_auto_message()

# Run the bot
Bot.run()
