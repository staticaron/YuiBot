from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from helpers import general_helper
import pdb

import config


class MongoManager:

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    user_collection: AsyncIOMotorCollection = None
    smash_collection: AsyncIOMotorCollection = None

    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(config.MONGO_SRV)
        self.db = self.client[config.DB]
        self.user_collection = self.db["user"]
        self.smash_collection = self.db["smash"]

    async def get_user(self, userID: str) -> dict:

        query = {
            "userID": userID
        }

        cursor = await self.user_collection.find_one(query)

        cursor["token"] = await general_helper.decrypt_token(cursor.get("token"))

        return cursor

    async def add_user(self, userID: str, anilistID: str, token: str) -> None:

        encrypted_token = await general_helper.encrypt_token(token)

        try:
            existing_user = await self.get_user(userID)

            if existing_user is not None:
                await self.update_user(userID, anilistID, token)
                return

            document = {
                "userID": userID,
                "anilistID": anilistID,
                "token": encrypted_token
            }

            await self.user_collection.insert_one(document)
        except Exception as e:
            print(e)

    async def update_user(self, userID: str, anilistID: str = None, token: str = None) -> None:

        try:
            query = {
                "userID": userID
            }

            updates = {}

            if anilistID is not None:
                updates["anilistID"] = anilistID

            encrypted_token = await general_helper.encrypt_token(token)

            if token is not None:
                updates["token"] = encrypted_token

            await self.user_collection.update_one(query, {"$set": updates})

        except Exception as e:
            print(e)

    async def remove_user(self, userID: str) -> None:

        delete_query = {
            "userID": userID
        }

        await self.user_collection.delete_one(delete_query)


manager: MongoManager = None

def init_motor():
    global manager

    try:
        manager = MongoManager()
    except Exception as e:
        print(e)
    else:
        print("Database Initialized")
