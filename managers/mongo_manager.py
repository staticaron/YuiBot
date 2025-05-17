from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from helpers import general_helper

import config


class MongoManager:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    user_collection: AsyncIOMotorCollection = None
    servers_collection: AsyncIOMotorCollection = None
    smash_collection: AsyncIOMotorCollection = None

    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(config.MONGO_SRV)
        self.db = self.client[config.DB]
        self.user_collection = self.db["user"]
        self.servers_collection = self.db["servers"]
        self.smash_collection = self.db["smash"]

    """ USER COLLECTION """

    async def get_user(self, userID: str) -> dict:
        query = {"userID": userID}

        cursor = await self.user_collection.find_one(query)

        if cursor is None:
            return None

        cursor["token"] = await general_helper.decrypt_token(cursor.get("token"))

        return cursor

    async def add_user(self, userID: str, anilistID: str, token: str) -> None:
        encrypted_token = await general_helper.encrypt_token(token)

        try:
            existing_user = await self.get_user(userID)

            if existing_user is not None:
                await self.update_user(userID, anilistID, encrypted_token)
                return

            document = {
                "userID": userID,
                "anilistID": anilistID,
                "token": encrypted_token,
            }

            await self.user_collection.insert_one(document)
        except Exception as e:
            print(e)

    async def update_user(self, userID: str, anilistID: str = None, token: str = None) -> None:
        try:
            query = {"userID": userID}

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
        delete_query = {"userID": userID}

        await self.user_collection.delete_one(delete_query)

    """ SERVERS_COLLECTION  """

    async def get_server(self, server_id: int) -> dict:
        query = {"server_id": server_id}

        cursor = await self.servers_collection.find_one(query)

        if cursor is None:
            return None

        return cursor

    async def add_server(self, collection_item: dict) -> None:
        query = {"server_id": collection_item.get("server_id")}

        existing_server = await self.get_server(query["server_id"])

        if existing_server is not None:
            await self.servers_collection.replace_one(query, collection_item)
            return

        await self.servers_collection.insert_one(collection_item)

        # insert_one introduces unwanted _id to the collection
        del collection_item["_id"]

    async def update_server(self, server_id: int, updated_values: dict) -> dict:
        query = {"server_id": server_id}

        return await self.servers_collection.update_one(query, {"$set": updated_values})

    async def remove_server(self, server_id: int) -> None:
        self.servers_collection.delete_one({"server_id": server_id})


manager: MongoManager = None


def init_motor():
    global manager

    try:
        manager = MongoManager()
    except Exception as e:
        print(e)
    else:
        print("Database Initialized")
