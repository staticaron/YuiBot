from discord import Member
import requests

from managers import mongo_manager
from helpers import general_helper
from queries import fav_queries
from config import ANILIST_BASE, ERROR_COLOR

async def add_fav_character(user:Member, character_id:int):

    data = await mongo_manager.manager.get_user(str(user.id))
    character_id = int(character_id)

    resp = requests.post(url=ANILIST_BASE, json={
        "query" : fav_queries.character_query,
        "variables" : {
            "id" : character_id
        }
    },headers={
            "Authorization" : data["token"]
        }
    ).json()

    fav_data = resp["data"]

    if fav_data is None:
        return await general_helper.get_information_embed(
            title="Whoops!",
            description="The following error(s) occurred : ```{}```".format("\n\n".join([error["message"] for error in resp["errors"]])),
            color=ERROR_COLOR
        )

    return await general_helper.get_information_embed(
        title="Done",
        description="That CHARACTER was added to your favourites.")