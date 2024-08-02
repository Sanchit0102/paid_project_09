import motor.motor_asyncio
import config 

client = motor.motor_asyncio.AsyncIOMotorClient(config.DB_URL)
db = client[config.DB_NAME]
users = db.users

#insert user data
async def insert(user_id):
    user_det = {"_id": user_id}
    try:
        await users.insert_one(user_det)
    except:
        pass
        
# Total User
async def total_user():
    user = await users.count_documents({})
    return user

async def getid():
    all_users = users.find({})
    return all_users
