from discord import Embed, Member
from discord.ext import commands
from datetime import datetime
import requests
import jwt

from utils.errors.UserNotFound import UserNotFound
from utils.errors.InvalidToken import InvalidToken
from views.select_view import SelectPaginator
from managers import mongo_manager
from helpers import general_helper
from queries.search_queries import media_selection_query, character_selection_query
import config

"""Just a way to transmit paginator and ids at the same time. Please no bully"""


class MediaData:
    anilist_id: int = None
    mal_id: int = None
    type = None
    titles: list = None
    genre: list = None
    url: str = None
    image_link = None

    def __init__(self, media_id: int, mal_id: int, media_type: str = "ANIME", title: list = None, genre: list = None, url: str = None, image_link: str = None):
        self.anilist_id = media_id
        self.mal_id = mal_id
        self.type = media_type
        self.titles = title
        self.genre = genre
        self.url = url
        self.image_link = image_link

    def get_name(self):
        for title in self.titles:
            if title is not None:
                return title


class CharacterData:
    anilist_id: int = None
    titles: list = None
    url: str = None
    image_link: str = None

    def __init__(self, character_id: int, character_titles: list = None, url: str = None, image_link: str = None) -> None:
        self.anilist_id = character_id
        self.titles = character_titles
        self.url = url
        self.image_link = image_link

    def get_name(self) -> str:
        for i in self.titles:
            if i is not None:
                return i


class DataInclusivePaginator:
    paginator: SelectPaginator = None
    data_elements: list = None
    data_type: str = None

    def __init__(self, paginator, data_elements: list, data_type: str):
        self.paginator = paginator
        self.data_elements = data_elements
        self.data_type = data_type

    def length(self):
        return len(self.data_elements)

    async def get_error_embed(self):
        return await general_helper.get_information_embed(
            title="Damn",
            description="No {} were found for that input".format(
                self.data_type),
            color=config.ERROR_COLOR
        )


"""Returns an embed with specified details"""


async def get_information_embed(title: str, color=config.NORMAL_COLOR, url: str = None, description: str = None, user: Member = None, thumbnail_link: str = None, fields: list = None) -> Embed:

    embd: Embed = Embed(title=title, color=color)
    embd.timestamp = datetime.now()

    if url is not None:
        embd.url = url

    if description is not None:
        embd.description = description

    if user is not None:
        embd.set_footer(icon_url=user.avatar.url,
                        text="Requested by {}".format(user.name))

    if thumbnail_link is not None:
        embd.set_thumbnail(url=thumbnail_link)

    if fields is not None:
        for field in fields:
            if len(field) != 3:
                continue

            embd.add_field(
                name=field[0],
                value=field[1],
                inline=field[2]
            )

    return embd

"""Returns the aniList id from anilist username"""


async def get_id_from_anilist_username(username: str) -> int:

    query = """
        query($username:String){
            User(search:$username){
                id
            }
        }
    """

    variables = {
        "username": username
    }

    resp = requests.post(config.ANILIST_BASE, json={
                         "query": query, "variables": variables})

    try:
        return resp.json()["data"]["User"]["id"]
    except Exception as e:
        print(e)
        return None

"""Returns the aniList Id from token"""


async def get_id_from_token(token: str, user:Member) -> str:

    try:
        data = jwt.decode(token, options={"verify_signature": False})
    except:
        raise InvalidToken(user=user)

    return data["sub"]

"""Returns the aniList id from userID"""


async def get_id_from_userID(userID: str) -> str:

    data = await mongo_manager.manager.get_user(userID)

    if data is not None:
        return data["anilistID"]
    else:
        raise UserNotFound(user_id=userID)

"""Returns a formatted time string"""


async def get_time_str_from_seconds(seconds: int, front_limit: int = None, back_limit: int = None):

    time_str = ""

    days = seconds // 86400
    seconds = seconds - days * 86400
    hours = seconds // 3600
    seconds = seconds - hours * 3600
    minutes = seconds // 60
    seconds = seconds - minutes * 60

    time_vals = (days, hours, minutes, seconds)
    time_markers = ("days", "hours", "minutes", "seconds")

    if front_limit is not None and front_limit > len(time_markers):
        front_limit = len(time_markers)

    if back_limit is not None and back_limit > len(time_markers):
        back_limit = len(time_markers)

    if front_limit is not None:
        for i in range(len(time_markers) - ((len(time_markers) - front_limit))):
            if time_vals[i] > 0:
                time_str += "{} {} ".format(time_vals[i], time_markers[i])

        return (time_str if time_str != "" else "1 seconds")

    for i in range(len(time_vals)):
        if time_vals[i] > 0:
            time_str += "{} {} ".format(time_vals[i], time_markers[i])

    return (time_str if time_str != "" else "1 seconds")

"""Check whether the user is registered with AniList account or not"""


async def validate_user(ctx: commands.Context):

    command_user = ctx.author

    data = await mongo_manager.manager.get_user(str(command_user.id))

    if data is None:
        return False

    return True

"""Short Cooldown Decorator"""


def short_cooldown():

    return commands.cooldown(rate=1, per=5, type=commands.BucketType.user)

def long_cooldown():

    return commands.cooldown(rate=2, per=5*60, type=commands.BucketType.user)


"""Returns a list of medias to select from"""


async def get_media_selection_paginator(media_name: str, select_callback: callable, media_type="ANIME") -> DataInclusivePaginator:

    variables = {
        "search": media_name,
        "type": media_type
    }

    anime_resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query": media_selection_query,
            "variables": variables
        }
    ).json()

    anime_data = anime_resp["data"]["Page"]["media"]

    pages = []
    media_list = []

    for page_data in anime_data:
        embd = Embed(
            title="Which {} are you talking about?".format(media_type),
            color=config.NORMAL_COLOR
        )

        embd.description = "**Name** : [{name}]({url})\n**Episodes** : {episodes}\n**Status** : {status}".format(
            name=(page_data["title"]["english"] if page_data["title"]
                  ["english"] is not None else page_data["title"]["romaji"]),
            url=page_data["siteUrl"],
            episodes=page_data["episodes"],
            status=page_data["status"]
        )

        genres = ("\n".join(["{bullet}**{genre}**".format(bullet=config.BULLET_EMOTE, genre=genre)
                  for genre in page_data["genres"]]) if len(page_data["genres"]) > 0 else None)
        embd.add_field(
            name="Genres",
            value=genres,
            inline=False
        )

        embd.set_thumbnail(url=page_data["coverImage"]["medium"])

        pages.append(embd)
        media_list.append(MediaData(page_data["id"], page_data["idMal"]))

    if len(pages) > 0:
        paginator = SelectPaginator(pages, select_callback)
    else:
        paginator = None

    return DataInclusivePaginator(paginator, media_list, media_type)

"""Returns a list of characters to select from"""


async def get_character_selection_paginator(character_name: str, select_callback: callable) -> DataInclusivePaginator:

    variables = {
        "name": character_name
    }

    ch_response = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query": character_selection_query,
            "variables": variables
        }
    ).json()

    ch_data = ch_response["data"]["Page"]["characters"]

    pages = []
    media_list = []

    for page_data in ch_data:
        embd = Embed(
            title="Which CHARACTER are you talking about?",
            color=config.NORMAL_COLOR
        )

        embd.description = "**Name** : [{name}]({url}), {native}\n**Gender** : {gender}\n**Age** : {age}\n**Date Of Birth** : {dob}\n**Favorites** : {favorites}".format(
            name=page_data["name"]["full"],
            native=page_data["name"]["native"],
            url=page_data["siteUrl"],
            favorites=page_data["favourites"],
            age=page_data["age"],
            gender=page_data["gender"],
            dob="{d} {m}".format(
                d=page_data["dateOfBirth"]["day"], m=page_data["dateOfBirth"]["month"])
        )

        embd.set_thumbnail(url=page_data["image"]["medium"])

        pages.append(embd)
        media_list.append(CharacterData(page_data["id"]))

    if len(pages) > 0:
        paginator = SelectPaginator(pages, select_callback)
    else:
        paginator = None

    return DataInclusivePaginator(paginator, media_list, "CHARACTER")
