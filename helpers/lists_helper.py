import json

import httpx
from discord import Embed, Member, User

import config
from helpers import general_helper
from managers import mongo_manager
from queries.fav_queries import *
from queries.list_queries import list_query
from queries.media_queries import media_status_query
from utils.errors.UserNotFound import UserNotFound
from views.scroller import Scroller

all_lists = [
    "ptw",
    "ptr",
    "planning",
    "crt",
    "current",
    "watching",
    "wtc",
    "reading",
    "comp",
    "completed",
    "drp",
    "dropped",
    "fav",
    "favorite",
]

lists = {
    "ptw": "PLANNING",
    "ptr": "PLANNING",
    "planning": "PLANNING",
    "crt": "CURRENT",
    "current": "CURRENT",
    "wtc": "CURRENT",
    "watching": "CURRENT",
    "reading": "CURRENT",
    "comp": "COMPLETED",
    "completed": "COMPLETED",
    "drp": "DROPPED",
    "dropped": "DROPPED",
    "psd": "PAUSED",
    "paused": "PAUSED",
}

"""Adds specified anime to the specified list"""


async def add_to_list(
    list_name: str, mediaID: int, user: User | Member, media_type: str = "ANIME"
) -> Embed:

    lst = lists[list_name]

    anilist_user = await mongo_manager.manager.get_user(str(user.id))
    if anilist_user is None:
        return await general_helper.get_information_embed(
            "User Not Found!", config.ERROR_COLOR, None, "Try Logging in again"
        )

    token = anilist_user["token"]

    async with httpx.AsyncClient() as client:
        list_resp = await client.post(
            url=config.ANILIST_BASE,
            json={
                "query": media_status_query,
                "variables": {"id": mediaID, "list": lst},
            },
            headers={"Authorization": token},
        )

        list_resp_raw = json.loads(list_resp.text)
        if list_resp_raw["data"]["SaveMediaListEntry"] is None:
            return await general_helper.get_information_embed(
                title="Whoops",
                description="The following error occurred : ```{}```".format(
                    list_resp_raw["error"]["message"]
                ),
                color=config.ERROR_COLOR,
            )

    return await general_helper.get_information_embed(
        title="Done", description=f"{media_type} was added to your `{lst}` list."
    )


async def add_to_fav(
    mediaID: int, user: User | Member, media_type: str = "ANIME"
) -> Embed:

    data = await mongo_manager.manager.get_user(str(user.id))
    if data is None:
        raise UserNotFound()

    entity_type = ""

    entity_type = "anime"
    fav_query = anime_query

    if media_type == "MANGA":
        entity_type = "manga"
        fav_query = manga_query
    elif media_type == "CHARACTER":
        entity_type = "characters"
        fav_query = character_query

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url=config.ANILIST_BASE,
            json={"query": fav_query, "variables": {"id": mediaID}},
            headers={"Authorization": data["token"]},
        )

        resp_raw = json.loads(resp.text)
        fav_data = resp_raw["data"]

        if fav_data is None or fav_data == {}:
            return await general_helper.get_information_embed(
                title="Whoops!",
                description="The following error(s) occurred : ```{}```".format(
                    "\n".join([error["message"] for error in resp_raw["errors"]])
                ),
                color=config.ERROR_COLOR,
            )

        new_fav_list = [
            fav["id"] for fav in fav_data["ToggleFavourite"][entity_type]["nodes"]
        ]

        return await general_helper.get_information_embed(
            title="Done",
            description="`{}` was **{}** ".format(
                media_type,
                "added to Favorites"
                if int(mediaID) in new_fav_list
                else "removed from Favorites",
            ),
        )


async def get_list_paginator(
    target: User | Member, media_type: str = "ANIME", list_name: str = "CURRENT"
):

    anilistID = await general_helper.get_id_from_userID(str(target.id))

    if anilistID is None:
        raise UserNotFound(user=target)

    async with httpx.AsyncClient() as client:
        list_resp = await client.post(
            url=config.ANILIST_BASE,
            json={
                "query": list_query,
                "variables": {
                    "id": anilistID,
                    "status": list_name,
                    "media": media_type,
                },
            },
        )

        list_resp_raw = json.loads(list_resp.text)
        list_data = None

        for i in list_resp_raw["data"]["MediaListCollection"]["lists"]:
            if i["isCustomList"] is False:
                list_data = i

        if list_data is None:
            return None

        entries = list_data["entries"]
        entries_size = len(entries)

        pages = []

        MAX_LISTINGS_PER_PAGE = 10
        current_listing_count = 0

        current_embed = (
            await general_helper.get_information_embed(
                title=list_data["name"] + " list",
                description=f"Total : {len(entries)}\n\n",
            )
        ).set_thumbnail(
            url=list_resp_raw["data"]["MediaListCollection"]["user"]["avatar"]["medium"]
        )

        for i in range(entries_size):
            current_listing_count += 1

            if current_listing_count > MAX_LISTINGS_PER_PAGE:
                current_listing_count = 1
                pages.append(current_embed)

                current_embed = (
                    await general_helper.get_information_embed(
                        title=list_data["name"] + " list",
                        description=f"Total : {entries_size}\n\n",
                    )
                ).set_thumbnail(
                    url=list_resp_raw["data"]["MediaListCollection"]["user"]["avatar"][
                        "medium"
                    ]
                )

            current_title = (
                entries[i]["media"]["title"]["english"]
                if entries[i]["media"]["title"]["english"] is not None
                else entries[i]["media"]["title"]["romaji"]
            )

            current_embed.description = (
                "{bullet} [{name}]({url}) - {progress}/{total}\n".format(
                    bullet=config.BULLET_EMOTE,
                    name=current_title,
                    url=entries[i]["media"]["siteUrl"],
                    progress=entries[i]["progress"],
                    total="{}".format(
                        entries[i]["media"]["episodes"]
                        if media_type == "ANIME"
                        else entries[i]["media"]["chapters"]
                    ),
                )
            )

            if i >= entries_size - 1:
                pages.append(current_embed)

    if len(pages) > 0:
        return Scroller(pages, True)
    else:
        return None


async def get_fav_paginator(target: User | Member, fav_type: str) -> Scroller | None:

    fav_query = anime_query if fav_type == "ANIME" else manga_query

    anilistID = await general_helper.get_id_from_userID(str(target.id))

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url=config.ANILIST_BASE,
            json={"query": fav_query, "variables": {"userID": anilistID}},
        )

        resp_raw = json.loads(resp.text)

        entries = resp_raw["data"]["User"]["favourites"][f"{fav_type.lower()}"][
            "nodes"
        ]  # List of media elements
        entries_size = len(entries)

        MAX_ENTRIES_PER_PAGE = 10
        current_entries_count = 0

        pages = []

        current_embd = await general_helper.get_information_embed(
            title=f"Favourite {fav_type.capitalize()}",
            description=f"Total : {len(entries)} \n\n",
        )

        for current_entry_count, i in enumerate(range(entries_size)):
            if current_entries_count > MAX_ENTRIES_PER_PAGE:
                pages.append(current_embd)
                current_embd = await general_helper.get_information_embed(
                    title=f"Favourite {fav_type.capitalize()}",
                    description=f"Total : {entries_size} \n\n",
                )

            title = (
                entries[i]["title"]["english"]
                if entries[i]["title"]["english"] is not None
                else entries[i]["title"]["romaji"]
            )
            current_embd.description = "{bullet} [{name}]({url}) \n".format(
                bullet=config.BULLET_EMOTE, name=title, url=entries[i]["siteUrl"]
            )

            if i >= entries_size - 1:
                pages.append(current_embd)

    if len(pages) > 0:
        return Scroller(pages, show_all_btns=True)
    else:
        return None
