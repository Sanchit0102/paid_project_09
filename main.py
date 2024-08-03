import os
import time
import pytz
import config
import logging
import requests
from flask import Flask
from threading import Thread
from pyrogram.errors import FloodWait
from pyrogram import Client, filters, errors, enums
from database import insert, total_user, getid, delete
from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


# ==========================[ Server Client ]=============================== # 

Bot = Client(
    "Trading Bot",
    bot_token=config.BOT_TOKEN,
    api_id=config.API_ID,
    api_hash=config.API_HASH
)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:5000")
app = Flask(__name__)

@app.route('/alive')
def alive():
    return "I am alive!"

def ping_self():
    url = f"{RENDER_EXTERNAL_URL}/alive"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info("Ping successful!")
        else:
            logging.error(f"Ping failed with status code {response.status_code}")
    except Exception as e:
        logging.error(f"Ping failed with exception: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler(timezone=pytz.utc)
    scheduler.add_job(ping_self, 'interval', minutes=3)
    scheduler.start()

def run_flask():
    app.run(host='0.0.0.0', port=10000)


# ==========================[ Start cmd Text ]=============================== # 

user_ids = {}

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
    user_data = message.from_user.id
    user_ids[user_data] = True
    await message.reply_photo(
        photo=config.START_IMG,
        caption=config.START_TEXT,
        parse_mode=enums.ParseMode.HTML,
        reply_markup=START_BUTTONS
    )

# # ==========================[ send After 2 Hr ]=============================== # 

# # Function to send broadcast message

async def send_broadcast_message(Bot):
    users = await user_ids # getid()
    user_ida = [user.id for users in user_ids]
    # for user_id in users:
    await Bot.send_photo(
        user_ida,
        photo=config.REPEAT_IMG,
        config=config.REPEAT_TXT,
        parse_mode=enums.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Join Now 🔥", url=f"https://t.me/+oMv-bxaGMXVkNmE0")]])
    )


async def schedule_broadcast():
    while True:
        await send_broadcast_message(Bot)
        await asyncio.sleep(300)  # Sleep for 2 hours (7200 seconds)

# Start the asyncio event loop
asyncio.get_event_loop().run_until_complete(schedule_broadcast())

# ==========================[ Bot Run ]=============================== # 

@Bot.on_message(filters.private & filters.user(config.ADMIN) & filters.command(["broadcast"]))
async def broadcast(bot, message):
    if (message.reply_to_message):
        ds = await message.reply_text("Bot Processing.\nI am checking all bot users.")
        all_users = await getid()
        tot = await total_user()
        success = 0
        failed = 0
        deactivated = 0
        blocked = 0
        await ds.edit(f"bot ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ started...")
        async for user in all_users:
            try:
                time.sleep(1)
                await message.reply_to_message.copy(user['_id'])
                success += 1
            except errors.InputUserDeactivated:
                deactivated +=1
                await delete({"_id": user['_id']})
            except errors.UserIsBlocked:
                blocked +=1
                await delete({"_id": user['_id']})
            except Exception as e:
                failed += 1
                await delete({"_id": user['_id']})
                pass
            try:
                await ds.edit(f"<u>ʙʀᴏᴀᴅᴄᴀsᴛ ᴘʀᴏᴄᴇssɪɴɢ</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {tot}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")
            except FloodWait as e:
                await asyncio.sleep(e.x)
        await ds.edit(f"<u>ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</u>\n\n• ᴛᴏᴛᴀʟ ᴜsᴇʀs: {tot}\n• sᴜᴄᴄᴇssғᴜʟ: {success}\n• ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: {blocked}\n• ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs: {deactivated}\n• ᴜɴsᴜᴄᴄᴇssғᴜʟ: {failed}")


# Function to send auto messages every 2 hours to users who started the bot
# def send_auto_message():
#     while True:
#         time.sleep(300)  # 2 hours interval
#         users = get_users_to_send_message()  # Implement this function to get users who started the bot
#         for user in users:
#             BOT.send_message(
#                 user,
#                 photo=config.REPEAT_IMG,
#                 caption=config.REPEAT_TXT,
#                 disable_web_page_preview=True,
#                 reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Join Now 🔥", url=f"https://t.me/+oMv-bxaGMXVkNmE0")]])
#             )

# # Start the auto message sender
# send_auto_message()

# Run the bot
Thread(target=run_flask).start()
start_scheduler()
Bot.run()
