from discord import Embed, Member
import enum

import requests

from managers import mongo_manager
from helpers import general_helper
from queries import character_queries, search_queries, studio_queries
import config

class MediaType(enum.Enum):
    ANIME = 0,
    MANGA = 1

async def get_error_embed(data_raw:dict) -> Embed:
    errors = [error["message"] for error in data_raw["errors"]]
    return await general_helper.get_information_embed(title="Error Occurred!", color=config.ERROR_COLOR, description="{}{}".format(config.BULLET_EMOTE, "\n{}".format(config.BULLET_EMOTE).join(errors)))

async def get_media_details(name:str, type:MediaType, user:Member) -> dict:
    
    anilist_user = await mongo_manager.manager.get_user(str(user.id))

    if type is MediaType.ANIME:
        query = search_queries.anime_query
    else:
        query = search_queries.manga_query

    resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query" : query,
            "variables" : {
                "search" : name
            }
        },
        headers={
            "Authorization" : anilist_user["token"]
        }
    )

    return resp.json()

async def get_character_details(name:str) -> dict:

    variables = {
        "search" : name
    }

    resp = requests.post(config.ANILIST_BASE, json={"query" : character_queries.query, "variables" : variables})

    return resp.json()

async def get_studio_details(name:str) -> dict:

    variables = {
        "search" : name
    }

    resp = requests.post(config.ANILIST_BASE, json={"query" : studio_queries.query, "variables" : variables})

    return resp.json()

async def get_anime_details_embed(name:str, user:Member) -> Embed:

    data_raw = await get_media_details(name, MediaType.ANIME, user)
    data = data_raw["data"]["Media"]

    if data is None:
        return await get_error_embed(data_raw)

    title = "#{id} - {eng_name} {is_adult}".format(id=data["id"], eng_name=(data["title"]["english"] if data["title"]["english"] is not None else data["title"]["romaji"]), is_adult=config.ADULT_CONTENT_EMOTE if data["isAdult"] else "")

    embd:Embed = Embed(title=title, color=config.NORMAL_COLOR, url=data["siteUrl"])
    embd.description = data["description"][:300] + "... [read more]({})".format(data["siteUrl"])
    embd.set_thumbnail(url=data["coverImage"]["large"])


    titles = [x if x is not None else "" for x in list(data["title"].values())]
    embd.add_field(
        name="Titles",
        value="\n".join(titles),
        inline=True
    )

    genres = ("\n".join(list(data["genres"])) if len(list(data["genres"])) > 0 else None)
    embd.add_field(
        name="Genres",
        value=genres,
        inline=True
    )

    startDate = [str(x) for x in list(data["startDate"].values())]
    embd.add_field(
        name="Start Date",
        value="\n".join(startDate),
        inline=True
    )

    embd.add_field(
        name="Average Score",
        value=str(data["averageScore"]),
        inline=True
    )

    embd.add_field(
        name="Mean Score",
        value=str(data["meanScore"]),
        inline=True
    )

    embd.add_field(
        name="Favourites",
        value=str(data["favourites"]),
        inline=True
    )

    embd.add_field(
        name="Episodes",
        value=str(data["episodes"]),
        inline=True
    )

    embd.add_field(
        name="Duration",
        value=str(data["duration"]),
        inline=True
    )

    embd.add_field(
        name="Status",
        value=data["status"],
        inline=True
    )

    embd.add_field(
        name="Format",
        value=data["format"],
        inline=True
    )

    studios = (data["studios"]["nodes"] if len(data["studios"]["nodes"]) <=3 else data["studios"]["nodes"][:3])
    studios_str = "\n".join(["[{name}]({url})".format(name=studio["name"], url=studio["siteUrl"] if studio["siteUrl"] is not None else "") for studio in studios])
    embd.add_field(
        name="Studios",
        value=studios_str,
        inline=True
    )

    trailer_link = ("[click here](https://www.youtube.com/watch?v={})".format(data["trailer"]["id"]) if data["trailer"] is not None and data["trailer"]["site"] == "youtube" else "Not Available")
    embd.add_field(
        name="Trailer",
        value=trailer_link,
        inline=True
    )

    #### Footer
    isFav = (f"🔘FAV : Yes" if data["isFavourite"] is True else "")
    status = ("STATUS : " + data["mediaListEntry"]["status"] if data["mediaListEntry"]  is not None else "")
    score = ((f"🔘SCORE : " + str(data["mediaListEntry"]["score"]) if data["mediaListEntry"]["score"] != 0 else "") if data["mediaListEntry"]  is not None else "")
    progress = (f"🔘PROGRESS : " + str(data["mediaListEntry"]["progress"] if data["mediaListEntry"]  is not None else ""))
    total = ("/" + str(data["mediaListEntry"]["media"]["episodes"] if data["mediaListEntry"]  is not None else ""))

    if not (isFav == "" and status == ""):
        embd.set_footer(text="{status}{fav}{score}{progress}{total}".format(status=status, fav=isFav, score=score, progress=progress, total=total))

    return embd

async def get_manga_details_embed(name:str, user:Member) -> Embed:
    data_raw = await get_media_details(name, MediaType.MANGA, user)
    data = data_raw["data"]["Media"]

    if data is None:
        return await get_error_embed(data_raw)

    title = "#{id} - {eng_name} {is_adult}".format(id=data["id"], eng_name=data["title"]["english"], is_adult=config.ADULT_CONTENT_EMOTE if data["isAdult"] else "")

    embd:Embed = Embed(title=title, color=config.NORMAL_COLOR, url=data["siteUrl"])
    embd.description = data["description"][:200] + "... [read more]({})".format(data["siteUrl"])
    embd.set_thumbnail(url=data["coverImage"]["large"])

    titles = [x if x is not None else "" for x in list(data["title"].values())]
    embd.add_field(
        name="Titles",
        value="\n".join(titles),
        inline=True
    )

    embd.add_field(
        name="Genres",
        value="\n".join(list(data["genres"])),
        inline=True
    )

    startDate = [str(x) for x in list(data["startDate"].values())]
    embd.add_field(
        name="Start Date",
        value="\n".join(startDate),
        inline=True
    )

    embd.add_field(
        name="Average Score",
        value=str(data["averageScore"]),
        inline=True
    )

    embd.add_field(
        name="Mean Score",
        value=str(data["meanScore"]),
        inline=True
    )

    embd.add_field(
        name="Favorites",
        value=str(data["favourites"]),
        inline=True
    )

    embd.add_field(
        name="Chapters",
        value=str(data["chapters"]),
        inline=True
    )

    embd.add_field(
        name="Volumes",
        value=str(data["volumes"]),
        inline=True
    )

    embd.add_field(
        name="Status",
        value=data["status"],
        inline=True
    )

    embd.add_field(
        name="Format",
        value=data["format"],
        inline=True
    )

    studios = (data["studios"]["nodes"] if len(data["studios"]["nodes"]) <=3 else data["studios"]["nodes"][:3])
    studios_str = "\n".join(["[{name}]({url})".format(name=studio["name"], url=studio["siteUrl"] if studio["siteUrl"] is not None else "") for studio in studios])
    embd.add_field(
        name="Studios",
        value=studios_str,
        inline=True
    )

    trailer_link = ("[click here](https://www.youtube.com/watch?v={})".format(data["trailer"]["id"]) if data["trailer"] is not None and data["trailer"]["site"] == "youtube" else "Not Available")
    embd.add_field(
        name="Trailer",
        value=trailer_link,
        inline=True
    )

    #### Footer
    isFav = (f"🔘FAV : Yes" if data["isFavourite"] is True else "")
    status = ("STATUS : " + data["mediaListEntry"]["status"] if data["mediaListEntry"]  is not None else "")
    score = ((f"🔘SCORE : " + str(data["mediaListEntry"]["score"]) if data["mediaListEntry"]["score"] != 0 else "") if data["mediaListEntry"]  is not None else "")
    progress = (f"🔘PROGRESS : " + str(data["mediaListEntry"]["progress"] if data["mediaListEntry"]  is not None else ""))
    total = ("/" + str(data["mediaListEntry"]["media"]["chapters"] if data["mediaListEntry"]  is not None else ""))

    if not (isFav == "" and status == ""):
        embd.set_footer(text="{status}{fav}{score}{progress}{total}".format(status=status, fav=isFav, score=score, progress=progress, total=total))

    return embd

async def get_character_details_embed(name:str) -> Embed:

    data_raw = await get_character_details(name)
    data = data_raw["data"]["Character"]

    if data is None:
        return await get_error_embed(data_raw)

    title = "#{} - {}".format(data["id"], data["name"]["full"] if data["name"]["full"] is not None else data["name"]["native"])

    embd:Embed = Embed(title=title, color=config.NORMAL_COLOR, url=data["siteUrl"])
    embd.description = data["description"][:300] + "... *[read more]({})*".format(data["siteUrl"])

    embd.set_thumbnail(url=data["image"]["medium"])

    name_str = data["name"]["native"] + "\n"
    name_str += "\n".join(data["name"]["alternative"][:3])

    embd.add_field(
        name="Names",
        value=name_str,
        inline=True
    )

    embd.add_field(
        name="Gender",
        value=data["gender"],
        inline=True
    )

    embd.add_field(
        name="Favorites",
        value=data["favourites"],
        inline=True
    )

    embd.add_field(
        name="Age",
        value=data["age"],
        inline=True
    )

    dateOfBirth = [str(date) for date in list(data["dateOfBirth"].values())]
    embd.add_field(
        name="Date Of Birth",
        value="\n".join(dateOfBirth),
        inline=True
    )

    appearances_str = "\n".join(["[{name}]({url})".format(name=media["title"]["english"] if media["title"]["english"] is not None else media["title"]["romaji"], url=media["siteUrl"] if media["siteUrl"] is not None else "") for media in data["media"]["nodes"][:3]])
    embd.add_field(
        name="Appearances",
        value=appearances_str,
        inline=True
    )

    return embd

async def get_studio_details_embed(name:str) -> Embed:

    data_raw = await get_studio_details(name)   
    data = data_raw["data"]["Studio"]

    if data is None:
        return await get_error_embed(data_raw)

    title = "#{} - {}".format(data["id"], data["name"])

    embd:Embed = Embed(title=title, color=config.NORMAL_COLOR, url=data["siteUrl"])

    embd.description = "**Animation Studio ? : **" + ("Yes" if data["isAnimationStudio"] is True else "No")
    embd.description += "\n"
    embd.description += "**Favourites : **" + str(data["favourites"])

    work_str = ""
    medias = (data["media"]["nodes"] if len(data["media"]["nodes"]) <= 5 else data["media"]["nodes"][:6]) 
    for media in medias:
        work_str += "{bullet} [{name}]({url}) {dot} {format} {dot} {status} \n".format(bullet=config.BULLET_EMOTE, dot=config.DOT_EMOTE, name=media["title"]["english"] if media["title"]["english"] is not None else media["title"]["romaji"], url=media["siteUrl"], format=media["format"], status=media["status"])

    embd.add_field(
        name="Works ",
        value=work_str,
        inline=False
    )

    return embd
