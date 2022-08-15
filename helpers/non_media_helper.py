from discord import Member, Embed
import requests

from views.scroller import Scroller
from managers import mongo_manager
from helpers import general_helper
from queries import fav_queries
from config import ANILIST_BASE, ERROR_COLOR, BULLET_EMOTE

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

async def get_fav_character_scroller(user:Member) -> Scroller:

    anilist_id = await general_helper.get_id_from_userID(str(user.id))

    resp = requests.post(
        url=ANILIST_BASE,
        json={
            "query" : fav_queries.character_list_query,
            "variables" : {
                "userID" : anilist_id
            }
        }
    ).json()

    entries = resp["data"]["User"]["favourites"]["characters"]["nodes"] # List of character elements
    entries_size = len(entries)

    MAX_ENTRIES_PER_PAGE = 10
    current_entries_count = 0

    pages = []

    current_embd = Embed(
        title="Favourite Characters",
        description="Total : {} \n\n".format(len(entries))
    )

    for i in range(entries_size):

        current_entries_count += 1

        if current_entries_count > MAX_ENTRIES_PER_PAGE:
            pages.append(current_embd)
            current_embd = Embed(
                title="Favourite Characters",
                description="Total : {} \n\n".format(entries_size)
            )
            current_entries_count = 0

        full_name = entries[i]["name"]["full"]
        native_name = entries[i]["name"]["native"]
        current_embd.description += "{bullet} [{full_name}]({url}) {native_name} \n".format(bullet=BULLET_EMOTE, full_name=full_name, native_name=native_name, url=entries[i]["siteUrl"])

        if i >= entries_size - 1:
            pages.append(current_embd)

    if len(pages) > 0:
        return Scroller(pages, show_all_btns=True)
    else:
        return None