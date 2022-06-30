from discord import Embed
import enum

import requests

import config
from queries import media_queries, character_queries

class MediaType(enum.Enum):
    ANIME = 0,
    MANGA = 1

async def get_media_details(name:str, type:MediaType) -> dict:
    
    if type is MediaType.ANIME:
        query = media_queries.anime_query
    else:
        query = media_queries.manga_query

    variables = {
        "search" : name
    }

    resp = requests.post(config.ANILIST_BASE, json={"query" : query, "variables" : variables})

    return resp.json()

async def get_character_details(name:str) -> dict:

    variables = {
        "search" : name
    }

    resp = requests.post(config.ANILIST_BASE, json={"query" : character_queries.character_query, "variables" : variables})

    print(resp.text)

    return resp.json()


async def get_anime_details_embed(name:str) -> Embed:

    data = await get_media_details(name, MediaType.ANIME)
    data = data["data"]["Media"]

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

    embd.add_field(
        name="Season",
        value=data["seasonInt"],
        inline=True
    )

    trailer_link = ("[click here](https://www.youtube.com/watch?v={})".format(data["trailer"]["id"]) if data["trailer"] is not None and data["trailer"]["site"] == "youtube" else "Not Available")
    embd.add_field(
        name="Trailer",
        value=trailer_link,
        inline=True
    )

    return embd

async def get_manga_details_embed(name:str) -> Embed:
    data = await get_media_details(name, MediaType.MANGA)
    data = data["data"]["Media"]

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
        name="Favourites",
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

    embd.add_field(
        name="Season",
        value=data["seasonInt"],
        inline=True
    )

    trailer_link = ("https://www.youtube.com/watch?v={}".format(data["trailer"]["id"]) if data["trailer"]["site"] == "youtube" else "Not Available")
    embd.add_field(
        name="Trailer",
        value="[click here]({})".format(trailer_link),
        inline=True
    )

    return embd

async def get_character_details_embed(name:str) -> Embed:

    data = await get_character_details(name)
    data = data["data"]["Character"]

    if data is None:
        pass # return not found embed

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