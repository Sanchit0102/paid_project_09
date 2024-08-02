import os
import config
import time
import asyncio
from pyrogram import Client, filters, errors
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database import insert, total_user, getid, delete

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

# Bot.run()

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


@Bot.on_message(filters.private & filters.command(["start"]))
def start_command(client, message):
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
            BOT.send_message(
                user,
                photo=config.REPEAT_IMG,
                caption=config.REPEAT_TXT,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Join Now 🔥", url=f"https://t.me/+oMv-bxaGMXVkNmE0")]])
            )

# Start the auto message sender
send_auto_message()

# Run the bot
Bot.run()
