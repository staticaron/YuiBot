from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

import config

class MongoManager:
    
    client : AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    user_collection:AsyncIOMotorCollection = None

    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(config.MONGO_SRV)
        self.db = self.client[config.DB]
        self.user_collection = self.db["user"]

    async def get_user(self, userID:str) -> dict:

        query = {
            "userID" : userID
        }

        cursor = await self.user_collection.find_one(query)

        return cursor

    async def add_user(self, userID:str, anilistID:str, token:str) -> None:

        try:
            collection : AsyncIOMotorCollection = self.db["user"]

            existing_user = await self.get_user(userID)

            if existing_user is not None:
                await self.update_user(userID, anilistID, token)
                return

            document = {
                "userID" : userID,
                "anilistID" : anilistID,
                "token" : token
            }

            await collection.insert_one(document)
        except Exception as e:
            print(e)

    async def update_user(self, userID:str, anilistID:str=None, token:str=None) -> None:

        try:
            collection:AsyncIOMotorCollection = self.db["user"]

            query = {
                "userID" : userID
            }

            updates = {}

            if anilistID is not None:
                updates["anilistID"] = anilistID

            if token is not None:
                updates["token"] = token

            await collection.update_one(query, {"$set" : updates})
        except Exception as e:
            print(e)

manager:MongoManager = None

def init_motor():
    global manager

    try:
        manager = MongoManager()
    except Exception as e:
        print(e)
    else:
        print("Database Initialized")
    