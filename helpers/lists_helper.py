import requests
from discord import Embed, Member

from views.scroller import Scroller
from managers import mongo_manager
from helpers import general_helper
from queries.list_queries import list_query
from queries.media_queries import media_status_query
from queries.fav_queries import *
import config

all_lists = ["ptw", "ptr", "planning", "crt", "current", "watching", "wtc",
             "reading", "comp", "completed", "drp", "dropped", "fav", "favorite"]

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
}

"""Adds specified anime to the specified list"""


async def add_to_list(list_name: str, mediaID: int, user: Member, media_type: str = "ANIME") -> Embed:

    lst = lists[list_name]

    token = (await mongo_manager.manager.get_user(str(user.id)))["token"]

    list_resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query": media_status_query,
            "variables": {
                "id": mediaID,
                "list": lst
            }
        },
        headers={
            "Authorization": token
        }
    ).json()

    if list_resp["data"]["SaveMediaListEntry"] is None:
        return await general_helper.get_information_embed(
            title="Whoops",
            description="The following error occurred : ```{}```".format(
                list_resp["error"]["message"]),
            color=config.ERROR_COLOR
        )

    return await general_helper.get_information_embed(
        title="Done",
        description="{} was added to your `{}` list.".format(media_type, lst)
    )


async def add_to_fav(mediaID: int, user: Member, media_type: str = "ANIME"):

    data = await mongo_manager.manager.get_user(str(user.id))

    entity_type = ""

    if media_type == "ANIME":
        entity_type = "anime"
        fav_query = anime_query
    elif media_type == "MANGA":
        entity_type = "manga"
        fav_query = manga_query
    elif media_type == "CHARACTER":
        entity_type = "characters"
        fav_query = character_query

    resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query": fav_query,
            "variables": {
                "id": mediaID
            }
        },
        headers={
            "Authorization": data["token"]
        }
    ).json()

    fav_data = resp["data"]

    if fav_data is None:
        return await general_helper.get_information_embed(
            title="Whoops!",
            description="The following error(s) occurred : ```{}```".format(
                "\n".join([error["message"] for error in resp["errors"]])),
            color=config.ERROR_COLOR
        )

    new_fav_list = [fav["id"] for fav in fav_data["ToggleFavourite"][entity_type]["nodes"]]

    return await general_helper.get_information_embed(
        title="Done",
        description="`{}` was **{}** ".format(media_type, "added to Favorites" if int(mediaID) in new_fav_list else "removed from Favorites")
    )


async def get_list_paginator(target: Member, media_type: str = "ANIME", list_name: str = "CURRENT"):

    anilistID = await general_helper.get_id_from_userID(str(target.id))

    list_resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query": list_query,
            "variables": {
                "id": anilistID,
                "status": list_name,
                "media": media_type
            }
        }
    ).json()

    list_data = None

    for i in list_resp["data"]["MediaListCollection"]["lists"]:
        if i["isCustomList"] is False:
            list_data = i

    if list_data is None:
        return None

    entries = list_data["entries"]
    entries_size = len(entries)

    pages = []

    MAX_LISTINGS_PER_PAGE = 10
    current_listing_count = 0

    current_embed = (await general_helper.get_information_embed(
        title=list_data["name"] + " list",
        description="Total : {}\n\n".format(len(entries))
    )).set_thumbnail(url=list_resp["data"]["MediaListCollection"]["user"]["avatar"]["medium"])

    for i in range(entries_size):

        current_listing_count += 1

        if current_listing_count > MAX_LISTINGS_PER_PAGE:
            current_listing_count = 1
            pages.append(current_embed)

            current_embed = (await general_helper.get_information_embed(
                title=list_data["name"] + " list",
                description="Total : {}\n\n".format(entries_size)
            )).set_thumbnail(url=list_resp["data"]["MediaListCollection"]["user"]["avatar"]["medium"])

        current_title = (entries[i]["media"]["title"]["english"] if entries[i]["media"]
                         ["title"]["english"] is not None else entries[i]["media"]["title"]["romaji"])
        current_embed.description += "{bullet} [{name}]({url}) - {progress}/{total}\n".format(
            bullet=config.BULLET_EMOTE,
            name=current_title,
            url=entries[i]["media"]["siteUrl"],
            progress=entries[i]["progress"],
            total="{}".format(
                (entries[i]["media"]["episodes"] if media_type == "ANIME" else entries[i]["media"]["chapters"]))
        )

        if i >= entries_size - 1:
            pages.append(current_embed)

    if len(pages) > 0:
        return Scroller(pages, True)
    else:
        return None


async def get_fav_paginator(target: Member, fav_type: str) -> Scroller:

    if fav_type == "ANIME":
        fav_query = anime_list_query
    elif fav_type == "MANGA":
        fav_query = manga_list_query

    anilistID = await general_helper.get_id_from_userID(str(target.id))

    resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query": fav_query,
            "variables": {
                "userID": anilistID
            }
        }
    ).json()

    entries = resp["data"]["User"]["favourites"]["{}".format(
        fav_type.lower())]["nodes"]  # List of media elements
    entries_size = len(entries)

    MAX_ENTRIES_PER_PAGE = 10
    current_entries_count = 0

    pages = []

    current_embd = await general_helper.get_information_embed(
        title="Favourite {}".format(fav_type.capitalize()),
        description="Total : {} \n\n".format(len(entries))
    )

    for i in range(entries_size):

        current_entries_count += 1

        if current_entries_count > MAX_ENTRIES_PER_PAGE:
            pages.append(current_embd)
            current_embd = await general_helper.get_information_embed(
                title="Favourite {}".format(fav_type.capitalize()),
                description="Total : {} \n\n".format(entries_size)
            )

        title = (entries[i]["title"]["english"] if entries[i]["title"]
                 ["english"] is not None else entries[i]["title"]["romaji"])
        current_embd.description += "{bullet} [{name}]({url}) \n".format(
            bullet=config.BULLET_EMOTE, name=title, url=entries[i]["siteUrl"])

        if i >= entries_size - 1:
            pages.append(current_embd)

    if len(pages) > 0:
        return Scroller(pages, show_all_btns=True)
    else:
        return None
