from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pymongo import ReturnDocument

import config
from helpers import general_helper
from managers.logging_manager import get_logger

logger = get_logger()


class MongoManager:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(config.MONGO_SRV)
        self.db: AsyncIOMotorDatabase = self.client[config.DB]
        self.user_collection: AsyncIOMotorCollection = self.db["user"]
        self.servers_collection: AsyncIOMotorCollection = self.db["servers"]
        self.smash_collection: AsyncIOMotorCollection = self.db["smash"]

    """ USER COLLECTION """

    async def get_user(self, userID: str) -> dict | None:
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
        except Exception:
            logger.exception("Failed to add a user to the database!")

    async def update_user(self, userID: str, anilistID: str | None = None, token: str | None = None) -> None:
        """
        Update the AnilistID or Token or both in the database
        """

        try:
            query = {"userID": userID}

            updates = {}

            # if anilistID is passed, then update the anilistID
            if anilistID is not None:
                updates["anilistID"] = anilistID

            # if token is passed, then update the token as well
            if token is not None:
                encrypted_token = await general_helper.encrypt_token(token)

                if token is not None:
                    updates["token"] = encrypted_token

            await self.user_collection.update_one(query, {"$set": updates})

        except Exception:
            logger.exception(f"Failed to update the user {userID}")

    async def remove_user(self, userID: str) -> None:
        """
        Remove a user from the database
        """

        delete_query = {"userID": userID}
        await self.user_collection.delete_one(delete_query)

    """ SERVERS_COLLECTION  """

    async def get_server(self, server_id: int) -> dict | None:
        """
        Get Server Data from the database
        @param server_id The id of the server
        @return a dictionary containing the server data or None if data for the provided server_id doesn't exists
        """
        query = {"server_id": server_id}

        # return the server data dict or None
        return await self.servers_collection.find_one(query)

    async def add_server(self, collection_item: dict) -> None:
        """
        Add a Server Data to the database
        @param collection_item A dictionary containing the server data
        """

        query = {"server_id": collection_item.get("server_id")}

        server_id: str | None = query.get("server_id", None)
        if server_id is None:
            return

        existing_server = await self.get_server(server_id)
        if existing_server is not None:
            await self.servers_collection.replace_one(query, collection_item)
            return

        await self.servers_collection.insert_one(collection_item)

    async def update_server(self, server_id: int, updated_values: dict) -> dict:
        """
        Update a Server Data
        @param server_id id of the server where the updates apply
        @param updated_values A dictionary containing add the values that need to be updated! Only the values that need to be updated
        @return a dict containing the updated values
        """

        query = {"server_id": server_id}
        updated_results = await self.servers_collection.find_one_and_update(query, {"$set": updated_values}, return_document=ReturnDocument.AFTER)

        return updated_results

    async def remove_server(self, server_id: int) -> None:
        """
        Remove a server from the database
        """

        await self.servers_collection.delete_one({"server_id": server_id})


def init_motor():
    global manager

    try:
        manager = MongoManager()
    except Exception:
        logger.exception("Failed to Init MongoManager")
    else:
        logger.info("Database Initialized")
