from helpers import general_helper
from managers import mongo_manager


async def logout(userID: str):

    await mongo_manager.manager.remove_user(userID)

    return await general_helper.get_information_embed(
        title="Logged Out", description="You were successfully logged out. "
    )
