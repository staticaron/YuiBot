from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

import config

class MongoManager:
    
    client : AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(config.MONGO_SRV)
        self.db = self.client[config.DB]

    async def add_user(self, userID:str, anilistID:str, token:str) -> None:

        try:
            collection : AsyncIOMotorCollection = self.db["user"]

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

            updates = {
                "anilistID" : anilistID,
                "token" : token
            }

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
    