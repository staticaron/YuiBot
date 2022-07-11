import requests

from managers import mongo_manager
from helpers import general_helper
from config import ANILIST_BASE

async def logout(userID:str):

    await mongo_manager.manager.remove_user(userID)

    return await general_helper.get_information_embed(
        title="Logged Out",
        description="You were successfully logged out. "
    )