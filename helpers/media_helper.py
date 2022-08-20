from discord import Embed
import requests

from managers import mongo_manager
from helpers import general_helper
from queries.media_queries import progress_update_query
import config


async def set_progress(userID: str, mediaID: int, progress: int) -> Embed:

    anilist_user = await mongo_manager.manager.get_user(userID)

    resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query": progress_update_query,
            "variables": {
                "mediaID": mediaID,
                "progress": progress
            }
        },
        headers={
            "Authorization": anilist_user["token"]
        }).json()

    data = resp["data"]["SaveMediaListEntry"]

    title = (data["media"]["title"]["english"] if data["media"]["title"]
             ["english"] is not None else data["media"]["title"]["native"])

    return await general_helper.get_information_embed(
        title="Done",
        description="Progress of `{}` was set to **{}**".format(
            title, progress
        )
    )
