# (c) 𝚂𝙰𝙽𝙲𝙷𝙸𝚃 ♛⛧
import os, re
from os import getenv, environ
id_pattern = re.compile(r'^.\d+$') 
# ==========================[ Bot Config ]=============================== # 

API_ID = int(getenv('API_ID', 25833520))
API_HASH = str(getenv('API_HASH', '7d012a6cbfabc2d0436d7a09d8362af7'))
BOT_TOKEN = str(getenv('BOT_TOKEN' , '6738059809:AAFfYft25qo-iKP-XpgLgq9ZCyhKoew8994'))
START_IMG = "https://graph.org/file/8dc72eae13be09ff294ef.jpg"
REPEAT_IMG = "https://graph.org/file/e913a80094926b1bb9778.jpg"
CHANNEL_LINKS = ["https://t.me/channel1", "https://t.me/channel2", "https://t.me/channel3"]
DB_URL = "mongodb+srv://immortal:5412ascs@immortal.jehlw9n.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "tradingbot"
ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1562935405').split()]


# ==========================[ Start Text ]=============================== # 

START_TEXT = """<b>No wayyy!!!!! 🫡💰

210$ to 1,027$ in public group in only one session 😳🔥

This is the power of compounding 🔥💰

Next session is going to be held after 5 minutes.

LIMITED SEATS- 12 ONLY ⚠️‼️

Join now:- 😳🫡
https://t.me/+oMv-bxaGMXVkNmE0
https://t.me/+oMv-bxaGMXVkNmE0
https://t.me/+oMv-bxaGMXVkNmE0</b>"""

# ==========================[ Repeat Text ]=============================== # 

REPEAT_TXT = """<b>I have found a bug in quotex where i can win all the trades!! 😳📈

With me my telegram members are also making profits for FREE OF COST!! 💰🚀

Free Signal Start In 5 MIN Don't Miss The Chance Join The Channel Fast 👇👇

https://t.me/+oMv-bxaGMXVkNmE0
https://t.me/+oMv-bxaGMXVkNmE0
https://t.me/+oMv-bxaGMXVkNmE0
https://t.me/+oMv-bxaGMXVkNmE0</b>"""

# ==========================[ The End ! ]=============================== # 
