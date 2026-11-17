import json

import httpx
from discord import Member, User

from config import ANILIST_BASE, BULLET_EMOTE, ERROR_COLOR
from helpers import general_helper
from managers import mongo_manager
from queries import fav_queries
from utils.errors.UserNotFound import UserNotFound
from views.scroller import Scroller


async def add_fav_character(user: Member, character_id: int):

    anilist_user = await mongo_manager.manager.get_user(str(user.id))
    if anilist_user is None:
        raise UserNotFound(user)

    character_id = int(character_id)

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url=ANILIST_BASE,
            json={
                "query": fav_queries.character_query,
                "variables": {"id": character_id},
            },
            headers={"Authorization": anilist_user["token"]},
        )

    resp_json = json.loads(resp.text)
    fav_data = resp_json["data"]

    if fav_data is None:
        return await general_helper.get_information_embed(
            title="Whoops!",
            description="The following error(s) occurred : ```{}```".format(
                "\n\n".join([error["message"] for error in resp_json["errors"]])
            ),
            color=ERROR_COLOR,
        )

    return await general_helper.get_information_embed(
        title="Done", description="That CHARACTER was added to your favourites."
    )


async def get_fav_character_scroller(user: User | Member) -> Scroller | None:

    anilist_id = await general_helper.get_id_from_userID(str(user.id))

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url=ANILIST_BASE,
            json={
                "query": fav_queries.character_list_query,
                "variables": {"userID": anilist_id},
            },
        )

    resp_json = json.loads(resp.text)

    entries = resp_json["data"]["User"]["favourites"]["characters"][
        "nodes"
    ]  # List of character elements
    entries_size = len(entries)

    MAX_ENTRIES_PER_PAGE = 10
    current_entries_count = 0

    pages = []

    current_embd = await general_helper.get_information_embed(
        title="Favourite Characters", description=f"Total : {len(entries)} \n\n"
    )

    for i in range(entries_size):
        current_entries_count += 1

        if current_entries_count > MAX_ENTRIES_PER_PAGE:
            pages.append(current_embd)
            current_embd = await general_helper.get_information_embed(
                title="Favourite Characters", description=f"Total : {entries_size} \n\n"
            )
            current_entries_count = 0

        full_name = entries[i]["name"]["full"]
        native_name = entries[i]["name"]["native"]
        current_embd.description = (
            "{bullet} [{full_name}]({url}) {native_name} \n".format(
                bullet=BULLET_EMOTE,
                full_name=full_name,
                native_name=native_name,
                url=entries[i]["siteUrl"],
            )
        )

        if i >= entries_size - 1:
            pages.append(current_embd)

    if len(pages) > 0:
        return Scroller(pages, show_all_btns=True)
    else:
        return None
