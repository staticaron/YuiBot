from discord import Embed, Member
import enum

import requests

from views.scroller import Scroller
from managers import mongo_manager
from helpers import general_helper
from queries.search_queries import *
from queries.studio_queries import studio_query
import config


class MediaType(enum.Enum):
    ANIME = 0,
    MANGA = 1


async def get_error_embed(data_raw: dict) -> Embed:
    errors = [error["message"] for error in data_raw["errors"]]
    return await general_helper.get_information_embed(title="Error Occurred!", color=config.ERROR_COLOR, description="{}{}".format(config.BULLET_EMOTE, "\n{}".format(config.BULLET_EMOTE).join(errors)))

async def get_query_from_media_type_and_user(type, anilist_user):
    if type is MediaType.ANIME:
        if anilist_user is not None:
            query = anime_query_with_stats
        else:
            query = anime_query_without_stats
    else:
        if anilist_user is not None:
            query = manga_query_with_stats
        else:
            query = manga_query_without_stats
    return query

async def get_media_details(name: str, type: MediaType, user: Member) -> dict:

    anilist_user = await mongo_manager.manager.get_user(str(user.id))

    query = await get_query_from_media_type_and_user(type, anilist_user)

    try:
        resp = requests.post(
            url=config.ANILIST_BASE,
            json={
                "query": query,
                "variables": {
                    "search": name
                }
            },
            headers={
                "Authorization": anilist_user["token"]
            }
        )
    except:
        resp = requests.post(
            url=config.ANILIST_BASE,
            json={
                "query": query,
                "variables": {
                    "search": name
                }
            }
        )

    return resp.json()


async def get_character_details(name: str, user: Member) -> dict:

    anilist_user = await mongo_manager.manager.get_user(str(user.id))

    variables = {
            "search": name
        }

    if anilist_user is None:
        resp = requests.post(config.ANILIST_BASE, json={
                        "query": character_query_without_stats, 
                        "variables": variables
                    })
    else:
        resp = requests.post(config.ANILIST_BASE, json={
                        "query": character_query_with_stats, 
                        "variables": variables
                    }, 
                    headers={
                        "Authorization": anilist_user["token"]
                    })

    return resp.json()


async def get_studio_details(name: str) -> dict:

    variables = {
        "search": name
    }

    resp = requests.post(config.ANILIST_BASE, json={"query": studio_query, "variables": variables})

    return resp.json()

async def get_details_embd(data, title):
    details_embd: Embed = Embed(
        title="DETAILS - " + title,
        color=config.NORMAL_COLOR, 
        url=data["siteUrl"]
    )

    details_embd.description = data["description"][:300] + "... [read more]({})".format(data["siteUrl"])
    
    details_embd.set_thumbnail(url=data["coverImage"]["large"])

    titles = [x if x is not None else "" for x in list(data["title"].values())]

    details_embd.add_field(
        name="Titles",
        value="\n".join(titles),
        inline=True
    )

    genres = ("\n".join(list(data["genres"])) if len(list(data["genres"])) > 0 else None)
    details_embd.add_field(
        name="Genres",
        value=genres or "None",
        inline=True
    )

    startDate = [str(x) for x in list(data["startDate"].values())]
    details_embd.add_field(
        name="Start Date",
        value="\n".join(startDate) or "None",
        inline=True
    )

    details_embd.add_field(
        name="Average Score",
        value=str(data["averageScore"]) or "None",
        inline=True
    )

    details_embd.add_field(
        name="Mean Score",
        value=str(data["meanScore"]) or "None",
        inline=True
    )

    details_embd.add_field(
        name="Favourites",
        value=str(data["favourites"]) or "None",
        inline=True
    )

    details_embd.add_field(
        name="Episodes",
        value=str(data["episodes"]),
        inline=True
    )

    details_embd.add_field(
        name="Duration",
        value=str(data["duration"]) or "None",
        inline=True
    )

    details_embd.add_field(
        name="Status",
        value=data["status"] or "None",
        inline=True
    )

    details_embd.add_field(
        name="Format",
        value=data["format"] or "None",
        inline=True
    )

    studios = (data["studios"]["nodes"] if len(data["studios"]["nodes"]) <= 3 else data["studios"]["nodes"][:3])
    studios_str = "\n".join(["[{name}]({url})".format(name=studio["name"], url=studio["siteUrl"] if studio["siteUrl"] is not None else "") for studio in studios])
    details_embd.add_field(
        name="Studios",
        value=studios_str or "None",
        inline=True
    )

    trailer_link = ("[click here](https://www.youtube.com/watch?v={})".format(data["trailer"]["id"]) if data["trailer"] is not None and data["trailer"]["site"] == "youtube" else "Not Available")
    details_embd.add_field(
        name="Trailer",
        value=trailer_link,
        inline=True
    )

    # Footer
    try:
        isFav = (f"🔘FAV : Yes" if data["isFavourite"] is True else "")
        status = ("STATUS : " + data["mediaListEntry"]["status"] if data["mediaListEntry"] is not None else "")
        score = ((f"🔘SCORE : " + str(data["mediaListEntry"]["score"]) if data["mediaListEntry"]["score"] != 0 else "") if data["mediaListEntry"] is not None else "")
        progress = (f"🔘PROGRESS : " + str(data["mediaListEntry"]["progress"] if data["mediaListEntry"] is not None else ""))
        total = ("/" + str(data["mediaListEntry"]["media"]["episodes"] if data["mediaListEntry"] is not None else ""))

        if not (isFav == "" and status == ""):
            details_embd.set_footer(text="{status}{fav}{score}{progress}{total}".format(status=status, fav=isFav, score=score, progress=progress, total=total))
    except:
        pass
    return details_embd

async def get_tags_embd(data, title, isAdultAllowed:bool=False) -> Embed:
    tags_embd: Embed = Embed(
        title="TAGS - " + title,
        color=config.NORMAL_COLOR, 
        url=data["siteUrl"]
    )
    
    tags_embd.set_thumbnail(url=data["coverImage"]["large"])
    
    tags = data.get("tags", [])[:12]
    
    if len(tags) <= 0:
        tags_embd.description = "No Tags Found!"
        return tags_embd
    
    for tag in tags:
        if tag.get("isAdult") and not isAdultAllowed:
            continue
        
        tags_embd.add_field(
            name=tag.get("name", "not found!"),
            value="Similarity : " + str(tag.get("rank")) + "%"
        )
        
    return tags_embd

async def get_anime_details_embed(name: str, user: Member) -> Embed:

    data_raw = await get_media_details(name, MediaType.ANIME, user)
    data = data_raw["data"]["Media"]

    if data is None:
        return await get_error_embed(data_raw)

    title = "#{id} - {eng_name} {is_adult}".format(id=data["id"], eng_name=(data["title"]["english"] if data["title"]["english"] is not None else data["title"]["romaji"]), is_adult=" - 18+" if data["isAdult"] else "")

    details_embd = await get_details_embd(data, title)
    tags_embd = await get_tags_embd(data, title, data["isAdult"])
    
    return {
        "embeds" : {
            "details" : details_embd,
            "tags" : tags_embd
        },
        "isAdult" : data["isAdult"]
    }


async def get_manga_details_embed(name: str, user: Member) -> Embed:
    data_raw = await get_media_details(name, MediaType.MANGA, user)
    data = data_raw["data"]["Media"]

    if data is None:
        return await get_error_embed(data_raw)

    title = "#{id} - {eng_name} {is_adult}".format(
        id=data["id"], eng_name=data["title"]["english"], is_adult=" - 18+" if data["isAdult"] else "")

    embd: Embed = Embed(
        title=title, color=config.NORMAL_COLOR, url=data["siteUrl"])
    embd.description = data["description"][:200] + \
        "... [read more]({})".format(data["siteUrl"])
    embd.set_thumbnail(url=data["coverImage"]["large"])

    titles = [x if x is not None else "" for x in list(data["title"].values())]
    embd.add_field(
        name="Titles",
        value="\n".join(titles) or "None",
        inline=True
    )

    genres = list(data["genres"])
    if len(genres) <= 0:
        genres = ["None"]

    embd.add_field(
        name="Genres",
        value="\n".join(genres) or "None",
        inline=True
    )

    startDate = [str(x) for x in list(data["startDate"].values())]
    embd.add_field(
        name="Start Date",
        value="\n".join(startDate) or "None",
        inline=True
    )

    embd.add_field(
        name="Average Score",
        value=str(data["averageScore"]) or "None",
        inline=True
    )

    embd.add_field(
        name="Mean Score",
        value=str(data["meanScore"]) or "None",
        inline=True
    )

    embd.add_field(
        name="Favorites",
        value=str(data["favourites"]) or "None",
        inline=True
    )

    embd.add_field(
        name="Chapters",
        value=str(data["chapters"]) or "None",
        inline=True
    )

    embd.add_field(
        name="Volumes",
        value=str(data["volumes"]) or "None",
        inline=True
    )

    embd.add_field(
        name="Status",
        value=data["status"] or "None",
        inline=True
    )

    embd.add_field(
        name="Format",
        value=data["format"] or "None",
        inline=True
    )

    embd.add_field(
        name="Popularity",
        value=data["popularity"] or "None",
        inline=True
    )

    trailer_link = ("[click here](https://www.youtube.com/watch?v={})".format(data["trailer"]["id"])
                    if data["trailer"] is not None and data["trailer"]["site"] == "youtube" else "Not Available")
    embd.add_field(
        name="Trailer",
        value=trailer_link or "None",
        inline=True
    )

    try:
        # Footer
        isFav = (f"🔘FAV : Yes" if data["isFavourite"] is True else "")
        status = ("STATUS : " + data["mediaListEntry"]["status"] if data["mediaListEntry"] is not None else "")
        score = ((f"🔘SCORE : " + str(data["mediaListEntry"]["score"]) if data["mediaListEntry"]["score"] != 0 else "") if data["mediaListEntry"] is not None else "")
        progress = (f"🔘PROGRESS : " + str(data["mediaListEntry"]["progress"] if data["mediaListEntry"] is not None else ""))
        total = ("/" + str(data["mediaListEntry"]["media"]["chapters"] if data["mediaListEntry"] is not None else ""))

        if not (isFav == "" and status == ""):
            embd.set_footer(text="{status}{fav}{score}{progress}{total}".format(status=status, fav=isFav, score=score, progress=progress, total=total))
    except:
        #Don't set the footer if data is not available 
        pass

    return {
        "embed" : embd,
        "isAdult" : data["isAdult"]
    }


async def get_character_details_embed(name: str, user: Member) -> Embed:

    data_raw = await get_character_details(name, user)
    data = data_raw["data"]["Character"]

    if data is None:
        return await get_error_embed(data_raw)

    title = "#{} - {}".format(data["id"], data["name"]["full"]
                              if data["name"]["full"] is not None else data["name"]["native"])

    embd: Embed = Embed(
        title=title, color=config.NORMAL_COLOR, url=data["siteUrl"])
    embd.description = data["description"][:300] + \
        "... *[read more]({})*".format(data["siteUrl"])

    embd.set_thumbnail(url=data["image"]["medium"])

    name_str = data["name"]["native"] + "\n"
    name_str += "\n".join(data["name"]["alternative"][:3])

    embd.add_field(
        name="Names",
        value=name_str or "None",
        inline=True
    )

    embd.add_field(
        name="Gender",
        value=data["gender"] or "None",
        inline=True
    )

    embd.add_field(
        name="Favorites",
        value=data["favourites"] or "None",
        inline=True
    )

    embd.add_field(
        name="Age",
        value=data["age"] or "None",
        inline=True
    )

    dateOfBirth = [str(date) for date in list(data["dateOfBirth"].values())]
    embd.add_field(
        name="Date Of Birth",
        value="\n".join(dateOfBirth) or "None",
        inline=True
    )

    appearances_str = "\n".join(["[{name}]({url})".format(name=media["title"]["english"] if media["title"]["english"] is not None else media["title"]
                                ["romaji"], url=media["siteUrl"] if media["siteUrl"] is not None else "") for media in data["media"]["nodes"][:3]])
    embd.add_field(
        name="Appearances",
        value=appearances_str or "None",
        inline=True
    )
    
    try:
        if data["isFavourite"]:
            embd.set_footer(text="FAVORITE : Yes")
    except:
        pass

    return embd


async def get_studio_details_embed(name: str) -> Embed:

    data_raw = await get_studio_details(name)
    data = data_raw["data"]["Studio"]

    if data is None:
        return await get_error_embed(data_raw)

    title = "#{} - {}".format(data["id"], data["name"])

    embd: Embed = Embed(
        title=title, color=config.NORMAL_COLOR, url=data["siteUrl"])

    embd.description = "**Animation Studio ? : **" + \
        ("Yes" if data["isAnimationStudio"] is True else "No")
    embd.description += "\n"
    embd.description += "**Favourites : **" + str(data["favourites"])

    work_str = ""
    medias = (data["media"]["nodes"] if len(
        data["media"]["nodes"]) <= 5 else data["media"]["nodes"][:6])
    for media in medias:
        work_str += "{bullet} [{name}]({url}) {dot} {format} {dot} {status} \n".format(bullet=config.BULLET_EMOTE, dot=config.DOT_EMOTE, name=media["title"]
                                                                                       ["english"] if media["title"]["english"] is not None else media["title"]["romaji"], url=media["siteUrl"], format=media["format"], status=media["status"])

    embd.add_field(
        name="Works ",
        value=work_str,
        inline=False
    )

    return embd


async def get_top_by_genre(genres: list, media_type: str = "ANIME") -> Scroller:

    genres = [config.ALL_GENRE_ALTS[genre.lower()] for genre in genres]

    resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query": top_genre_query,
            "variables": {
                "genre": genres,
                "type": media_type
            }
        }
    ).json()

    data = resp["data"]["Page"]["media"]

    # TODO : check for data length 0

    pages = []

    embd = await general_helper.get_information_embed(
        title="Top {type} in {genre}".format(
            type=media_type, genre=", ".join(genres).upper()),
        description=""
    )

    MAX_PER_EMBED = 10
    entry_count = 1
    total_entry_count = 1

    for media in data:

        title = (media["title"]["english"] if media["title"]
                 ["english"] is not None else media["title"]["romaji"])
        embd.description += "{number}. [{name}]({link}) - {meanScore}".format(
            number=total_entry_count, name=title, link=media["siteUrl"], meanScore=media["meanScore"]) + "\n"

        entry_count += 1
        total_entry_count += 1

        if entry_count > MAX_PER_EMBED:
            entry_count = 1
            pages.append(embd)
            embd = await general_helper.get_information_embed(
                title="Top {type} in {genre}".format(
                    type=media_type, genre=", ".join(genres).capitalize()),
                description=""
            )

    return Scroller(embed_pages=pages, show_all_btns=True)
