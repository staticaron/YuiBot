import enum
import json

import httpx
from discord import Embed, Member, User

import config
from helpers import general_helper
from managers import mongo_manager
from managers.logging_manager import get_logger
from queries.search_queries import *
from queries.studio_queries import studio_query
from views.scroller import Scroller

logger = get_logger()


class MediaType(enum.Enum):
    ANIME = 0
    MANGA = 1


class ErrorResult:
    async def create_from_dict(self, raw: dict):
        self.raw = raw
        self.embd = await general_helper.get_error_embed(raw)

    async def create_from_values(self, message):
        self.raw = {"errors": [{"message": message}]}
        self.embd = await general_helper.get_error_embed(self.raw)

    async def get_messages(self) -> list:
        return [err["message"] for err in self.raw["errors"]]


class MediaResult:
    def __init__(self, data: dict, type: MediaType):
        self.raw = data.get("data", {}).get("Media", None)

        if self.raw is None:
            return

        self.id = self.raw.get("id", None)
        self.title = self.raw.get("title", None)
        self.is_adult = self.raw.get("isAdult", None)
        self.site_url = self.raw.get("siteUrl", None)
        self.description = self.raw.get("description", None)
        self.cover_image = self.raw.get("coverImage", {}).get("large", None)
        self.genres = self.raw.get("genres", None)
        self.start_date = self.raw.get("startDate", None)
        self.average_score = self.raw.get("averageScore", None)
        self.mean_score = self.raw.get("meanScore", None)
        self.favorites = self.raw.get("favourites", None)
        self.status = self.raw.get("status", None)
        self.format = self.raw.get("format", None)
        self.popularity = self.raw.get("popularity", None)
        self.trailer = self.raw.get("trailer", None)

        self.tags = self.raw.get("tags", [])

        self.is_fav = self.raw.get("isFavourite", None)
        self.media_list = self.raw.get("mediaListEntry", None)

        if type is MediaType.ANIME:
            self.episodes = self.raw.get("episodes", None)
            self.duration = self.raw.get("duration", None)
            self.studios = self.raw.get("studios", None)
        else:
            self.chapters = self.raw.get("chapters", None)
            self.volumes = self.raw.get("volumes", None)


class MediaEmbedResult:
    def __init__(self, embd: Embed, tags_embd: Embed, is_adult: bool = False):
        self.embd = embd
        self.tags_embd = tags_embd
        self.is_adult = is_adult


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


async def get_media_details(name: str, media_type: MediaType, user: User | Member) -> MediaResult | ErrorResult:
    """
    Get the media details using the user or bot token
    Bot token is used to perform the search if the user provided hasn't logged in

    @param name name of the media
    @param type type of the media, either ANIME or MANGA
    @param user user executing the command

    @return a dictionary containing the data
    """
    anilist_user = await mongo_manager.manager.get_user(str(user.id))

    query = await get_query_from_media_type_and_user(media_type, anilist_user)

    # if user is not present, use the bot token to perform the search
    if anilist_user is None:
        async with httpx.AsyncClient() as client:
            resp_raw = await client.post(
                url=config.ANILIST_BASE,
                json={"query": query, "variables": {"search": name}},
            )

        resp = json.loads(resp_raw.text)

    # If user is present, then use their token to perform the search
    else:
        async with httpx.AsyncClient() as client:
            resp_raw = await client.post(
                url=config.ANILIST_BASE,
                json={"query": query, "variables": {"search": name}},
                headers={"Authorization": anilist_user["token"]},
            )
        resp = json.loads(resp_raw.text)

    return MediaResult(resp, media_type)


async def get_character_details(name: str, user: User | Member) -> dict:
    anilist_user = await mongo_manager.manager.get_user(str(user.id))

    variables = {"search": name}

    if anilist_user is None:
        async with httpx.AsyncClient() as client:
            resp_raw = await client.post(
                config.ANILIST_BASE,
                json={"query": character_query_without_stats, "variables": variables},
            )

        resp = json.loads(resp_raw.text)

    else:
        async with httpx.AsyncClient() as client:
            resp_raw = await client.post(
                config.ANILIST_BASE,
                json={"query": character_query_with_stats, "variables": variables},
                headers={"Authorization": anilist_user["token"]},
            )

        resp = json.loads(resp_raw.text)

    return resp


async def get_studio_details(name: str, user: User | Member) -> dict:
    anilist_user = await mongo_manager.manager.get_user(str(user.id))

    variables = {"search": name}

    if anilist_user is None:
        async with httpx.AsyncClient() as client:
            resp_raw = await client.post(
                config.ANILIST_BASE,
                json={"query": studio_query, "variables": variables},
            )

        resp = json.loads(resp_raw.text)

    else:
        async with httpx.AsyncClient() as client:
            resp_raw = await client.post(
                config.ANILIST_BASE,
                json={"query": studio_query, "variables": variables},
                headers={"Authorization": anilist_user["token"]},
            )

        resp = json.loads(resp_raw.text)

    return resp


async def get_details_embd(data: MediaResult) -> Embed:
    title = "#{id} - {eng_name} {is_adult}".format(
        id=data.id,
        eng_name=data.title.get("english", data.title.get("romaji", "None")),
        is_adult=" - 18+" if data.is_adult else "",
    )

    details_embd: Embed = Embed(title="DETAILS - " + title, color=config.NORMAL_COLOR, url=data.site_url)

    details_embd.description = data.description[:300] + f"... [read more]({data.site_url})"

    details_embd.set_thumbnail(url=data.cover_image)

    titles = [x if x is not None else "" for x in list(data.title.values())]

    details_embd.add_field(name="Titles", value="\n".join(titles), inline=True)

    genres = "\n".join(list(data.genres)) if len(list(data.genres)) > 0 else None
    details_embd.add_field(name="Genres", value=genres or "None", inline=True)

    startDate = [str(x) for x in list(data.start_date.values())]
    details_embd.add_field(name="Start Date", value="\n".join(startDate) or "None", inline=True)

    details_embd.add_field(name="Average Score", value=str(data.average_score) or "None", inline=True)

    details_embd.add_field(name="Mean Score", value=str(data.mean_score) or "None", inline=True)

    details_embd.add_field(name="Favourites", value=str(data.favorites) or "None", inline=True)

    details_embd.add_field(name="Episodes", value=str(data.episodes), inline=True)

    details_embd.add_field(name="Duration", value=str(data.duration) or "None", inline=True)

    details_embd.add_field(name="Status", value=data.status or "None", inline=True)

    details_embd.add_field(name="Format", value=data.format or "None", inline=True)

    studios = data.studios["nodes"] if len(data.studios["nodes"]) <= 3 else data.studios["nodes"][:3]
    studios_str = "\n".join(
        [
            "[{name}]({url})".format(
                name=studio["name"],
                url=studio["siteUrl"] if studio["siteUrl"] is not None else "",
            )
            for studio in studios
        ]
    )
    details_embd.add_field(name="Studios", value=studios_str or "None", inline=True)

    trailer_link = "[click here](https://www.youtube.com/watch?v={})".format(data.trailer["id"]) if data.trailer is not None and data.trailer["site"] == "youtube" else "Not Available"
    details_embd.add_field(name="Trailer", value=trailer_link, inline=True)

    isFav = "🔘FAV : Yes" if data.is_fav is True else ""
    status = "STATUS : " + data.media_list["status"] if data.media_list is not None else ""
    score = ("🔘SCORE : " + str(data.media_list["score"]) if data.media_list["score"] != 0 else "") if data.media_list is not None else ""
    progress = "🔘PROGRESS : " + str(data.media_list["progress"] if data.media_list is not None else "")
    total = "/" + str(data.media_list["media"]["episodes"] if data.media_list is not None else "")

    if not (isFav == "" and status == ""):
        details_embd.set_footer(text=f"{status}{isFav}{score}{progress}{total}")

    return details_embd


async def get_tags_embd(data: MediaResult, isAdultAllowed: bool = False) -> Embed:
    """
    Get the tags embed for the media data provided

    @param data dictionary containing the media data
    @param title title of the media
    @param isAdultAllowed adult tags are allowed or not

    @return tag data embed
    """
    title = ""

    tags_embd: Embed = Embed(title="TAGS - " + title, color=config.NORMAL_COLOR, url=data.site_url)

    tags_embd.set_thumbnail(url=data.cover_image)

    tags = data.tags[:12]

    if len(tags) <= 0:
        tags_embd.description = "No Tags Found!"
        return tags_embd

    for tag in tags:
        if tag.get("isAdult") and not isAdultAllowed:
            continue

        tags_embd.add_field(
            name=tag.get("name", "not found!"),
            value="Similarity : " + str(tag.get("rank")) + "%",
        )

    return tags_embd


async def get_anime_details_embed(name: str, user: User | Member) -> MediaEmbedResult | ErrorResult:
    data: MediaResult | ErrorResult = await get_media_details(name, MediaType.ANIME, user)

    if isinstance(data, ErrorResult):
        error_result = ErrorResult()
        await error_result.create_from_dict(data.raw)
        return error_result

    if data.raw is None:
        error_result = ErrorResult()
        await error_result.create_from_values("Not Found!")
        return error_result

    details_embd = await get_details_embd(data)
    tags_embd = await get_tags_embd(data, data.is_adult)

    return MediaEmbedResult(details_embd, tags_embd, data.is_adult)


async def get_manga_details_embed(name: str, user: User | Member) -> MediaEmbedResult | ErrorResult:
    data: MediaResult | ErrorResult = await get_media_details(name, MediaType.MANGA, user)

    if isinstance(data, ErrorResult):
        error_result = ErrorResult()
        await error_result.create_from_dict(data.raw)
        return error_result

    if data.raw is None:
        error_result = ErrorResult()
        await error_result.create_from_values("Not Found!")
        return error_result

    title = "#{id} - {eng_name} {is_adult}".format(
        id=data.id,
        eng_name=data.title.get("english", data.title.get("romaji", "None")),
        is_adult=" - 18+" if data.is_adult else "",
    )

    embd: Embed = Embed(title=title, color=config.NORMAL_COLOR, url=data.site_url)
    embd.description = data.description[:200] + f"... [read more]({data.site_url})"
    embd.set_thumbnail(url=data.cover_image)

    titles = [x if x is not None else "" for x in list(data.title.values())]
    embd.add_field(name="Titles", value="\n".join(titles) or "None", inline=True)

    genres = list(data.genres)
    if len(genres) <= 0:
        genres = ["None"]

    embd.add_field(name="Genres", value="\n".join(genres) or "None", inline=True)

    startDate = [str(x) for x in list(data.start_date.values())]
    embd.add_field(name="Start Date", value="\n".join(startDate) or "None", inline=True)

    embd.add_field(name="Average Score", value=str(data.average_score) or "None", inline=True)

    embd.add_field(name="Mean Score", value=str(data.mean_score) or "None", inline=True)

    embd.add_field(name="Favorites", value=str(data.favorites) or "None", inline=True)

    embd.add_field(name="Chapters", value=str(data.chapters) or "None", inline=True)

    embd.add_field(name="Volumes", value=str(data.volumes) or "None", inline=True)

    embd.add_field(name="Status", value=data.status or "None", inline=True)

    embd.add_field(name="Format", value=data.format or "None", inline=True)

    embd.add_field(name="Popularity", value=data.popularity or "None", inline=True)

    trailer_link = "[click here](https://www.youtube.com/watch?v={})".format(data.trailer.get("id")) if data.trailer is not None and data.trailer["site"] == "youtube" else "Not Available"
    embd.add_field(name="Trailer", value=trailer_link or "None", inline=True)

    isFav = "🔘FAV : Yes" if data.is_fav is True else ""
    status = "STATUS : " + data.media_list["status"] if data.media_list is not None else ""
    score = ("🔘SCORE : " + str(data.media_list["score"]) if data.media_list["score"] != 0 else "") if data.media_list is not None else ""
    progress = "🔘PROGRESS : " + str(data.media_list["progress"] if data.media_list is not None else "")
    total = "/" + str(data.media_list["media"]["chapters"] if data.media_list is not None else "")

    if not (isFav == "" and status == ""):
        embd.set_footer(text=f"{status}{isFav}{score}{progress}{total}")

    tags_embed = await get_tags_embd(data, data.is_adult)

    return MediaEmbedResult(embd, tags_embed, data.is_adult)


async def get_character_details_embed(name: str, user: User | Member) -> Embed:
    data_raw = await get_character_details(name, user)
    data = data_raw["data"]["Character"]

    if data is None:
        return await general_helper.get_error_embed(data_raw)

    title = "#{} - {}".format(
        data["id"],
        data["name"]["full"] if data["name"]["full"] is not None else data["name"]["native"],
    )

    embd: Embed = Embed(title=title, color=config.NORMAL_COLOR, url=data["siteUrl"])
    embd.description = data["description"][:300] + "... *[read more]({})*".format(data["siteUrl"])

    embd.set_thumbnail(url=data["image"]["medium"])

    name_str = data["name"]["native"] + "\n"
    name_str += "\n".join(data["name"]["alternative"][:3])

    embd.add_field(name="Names", value=name_str or "None", inline=True)

    embd.add_field(name="Gender", value=data["gender"] or "None", inline=True)

    embd.add_field(name="Favorites", value=data["favourites"] or "None", inline=True)

    embd.add_field(name="Age", value=data["age"] or "None", inline=True)

    dateOfBirth = [str(date) for date in list(data["dateOfBirth"].values())]
    embd.add_field(name="Date Of Birth", value="\n".join(dateOfBirth) or "None", inline=True)

    appearances_str = "\n".join(
        [
            "[{name}]({url})".format(
                name=media["title"]["english"] if media["title"]["english"] is not None else media["title"]["romaji"],
                url=media["siteUrl"] if media["siteUrl"] is not None else "",
            )
            for media in data["media"]["nodes"][:3]
        ]
    )
    embd.add_field(name="Appearances", value=appearances_str or "None", inline=True)

    if "isFavorite" in data:
        embd.set_footer(text="FAVORITE : Yes")

    return embd


async def get_studio_details_embed(name: str, user: User | Member) -> Embed:
    data_raw = await get_studio_details(name, user)

    data = data_raw["data"]["Studio"]

    if data is None:
        return await general_helper.get_error_embed(data_raw)

    title = "#{} - {}".format(data["id"], data["name"])

    embd: Embed = Embed(title=title, color=config.NORMAL_COLOR, url=data["siteUrl"])

    embd.description = "**Animation Studio ? : **" + ("Yes" if data["isAnimationStudio"] is True else "No")
    embd.description += "\n"
    embd.description += "**Favourites : **" + str(data["favourites"])

    work_str = ""
    medias = data["media"]["nodes"] if len(data["media"]["nodes"]) <= 5 else data["media"]["nodes"][:6]
    for media in medias:
        work_str += "{bullet} [{name}]({url}) {dot} {format} {dot} {status} \n".format(
            bullet=config.BULLET_EMOTE,
            dot=config.DOT_EMOTE,
            name=media["title"]["english"] if media["title"]["english"] is not None else media["title"]["romaji"],
            url=media["siteUrl"],
            format=media["format"],
            status=media["status"],
        )

    embd.add_field(name="Works ", value=work_str, inline=False)

    return embd


async def get_top_by_genre(genres: tuple, media_type: str = "ANIME") -> Scroller:
    genres = tuple(config.ALL_GENRE_ALTS[genre.lower()] for genre in genres)

    async with httpx.AsyncClient() as client:
        resp_raw = await client.post(
            url=config.ANILIST_BASE,
            json={
                "query": top_genre_query,
                "variables": {"genre": genres, "type": media_type},
            },
        )

    resp = json.loads(resp_raw.text)

    data = resp["data"]["Page"]["media"]

    # TODO : check for data length 0

    pages = []

    embd: Embed = await general_helper.get_information_embed(
        title="Top {type} in {genre}".format(type=media_type, genre=", ".join(genres).upper()),
    )
    embd_description = ""

    MAX_PER_EMBED = 10
    entry_count = 1
    total_entry_count = 1

    for media in data:
        title = media["title"]["english"] if media["title"]["english"] is not None else media["title"]["romaji"]
        embd_description += f"{total_entry_count}. [{title}]({media.get('siteUrl', '')}) - {media.get('meanScore', '-')} \n"

        entry_count += 1
        total_entry_count += 1

        if entry_count > MAX_PER_EMBED:
            entry_count = 1
            embd.description = embd_description
            pages.append(embd)
            embd = await general_helper.get_information_embed(
                title="Top {type} in {genre}".format(type=media_type, genre=", ".join(genres).capitalize()),
                description="",
            )
            embd_description = ""

    return Scroller(embed_pages=pages, show_all_btns=True)
