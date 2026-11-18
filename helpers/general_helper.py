import json
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from functools import wraps

import httpx
import jwt
from cryptography.fernet import Fernet
from discord import Embed, Member, Message, User
from discord.ext import commands
from discord.ext.pages import Paginator

import config
from helpers import general_helper
from managers import mongo_manager
from managers.logging_manager import get_logger
from queries.search_queries import character_selection_query, media_selection_query
from utils.errors.InvalidToken import InvalidToken
from utils.errors.UserNotFound import UserNotFound
from views.select_view import SelectPaginator

logger = get_logger()

"""Just a way to transmit paginator and ids at the same time. Please no bully"""


class MediaData:
    def __init__(
        self,
        media_id: int,
        mal_id: int,
        media_type: str = "ANIME",
        title: list | None = None,
        genre: list | None = None,
        url: str | None = None,
        image_link: str | None = None,
    ):
        self.anilist_id = media_id
        self.mal_id = mal_id
        self.type = media_type
        self.titles = title
        self.genre = genre
        self.url = url
        self.image_link = image_link

    def get_name(self):
        if self.titles is None:
            return "Not Found!"

        for title in self.titles:
            if title is not None:
                return title

        return "Not Found!"


class CharacterData:
    def __init__(
        self,
        character_id: int,
        character_titles: list | None = None,
        url: str | None = None,
        image_link: str | None = None,
    ) -> None:
        self.anilist_id = character_id
        self.titles = character_titles
        self.url = url
        self.image_link = image_link

    def get_name(self) -> str:

        if self.titles is None:
            return "Not Found!"

        for title in self.titles:
            if title is not None:
                return title

        return "Not Found!"


class DataInclusivePaginator:
    def __init__(self, paginator, data_elements: list, data_type: str):
        self.paginator = paginator
        self.data_elements = data_elements
        self.data_type = data_type

    def length(self):
        return len(self.data_elements)

    async def get_error_embed(self):
        return await general_helper.get_information_embed(
            title="Damn",
            description=f"No {self.data_type} were found for that input",
            color=config.ERROR_COLOR,
        )


async def get_information_embed(
    title: str,
    color=config.NORMAL_COLOR,
    url: str | None = None,
    description: str | None = None,
    user: Member | None = None,
    thumbnail_link: str | None = None,
    fields: list | None = None,
) -> Embed:
    """Returns an embed with specified details"""

    embd: Embed = Embed(title=title, color=color)
    embd.timestamp = datetime.now(UTC)

    if url is not None:
        embd.url = url

    if description is not None:
        embd.description = description

    if user is not None and user.avatar is not None:
        embd.set_footer(icon_url=user.avatar.url, text=f"Requested by {user.name}")

    if thumbnail_link is not None:
        embd.set_thumbnail(url=thumbnail_link)

    if fields is not None:
        for field in fields:
            if len(field) != 3:
                continue

            embd.add_field(name=field[0], value=field[1], inline=field[2])

    return embd


async def get_id_from_anilist_username(username: str) -> int | None:
    """Returns the aniList id from anilist username"""

    query = """
        query($username:String){
            User(search:$username){
                id
            }
        }
    """

    variables = {"username": username}

    async with httpx.AsyncClient() as client:
        resp = await client.post(config.ANILIST_BASE, json={"query": query, "variables": variables})

        try:
            return resp.json()["data"]["User"]["id"]
        except Exception:  # nkqa: BLE001
            logger.exception("Failed to get the ID of the user")
            return None


async def get_id_from_token(token: str, user: User | Member) -> str:
    """Returns the aniList Id from token"""

    try:
        data = jwt.decode(token, options={"verify_signature": False})

    except Exception:  # noqa: BLE001
        raise InvalidToken(user=user)

    return data["sub"]


async def get_id_from_userID(userID: str) -> str:
    """Returns the aniList id from userID"""
    data = await mongo_manager.manager.get_user(userID)

    if data is not None:
        return data["anilistID"]
    else:
        raise UserNotFound(user_id=userID)


async def get_time_str_from_seconds(seconds: int, front_limit: int | None = None, back_limit: int | None = None):
    """Returns a formatted time string"""

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
        for i in range(len(time_markers) - (len(time_markers) - front_limit)):
            if time_vals[i] > 0:
                time_str += f"{time_vals[i]} {time_markers[i]} "

        return time_str if time_str != "" else "1 seconds"

    for i in range(len(time_vals)):
        if time_vals[i] > 0:
            time_str += f"{time_vals[i]} {time_markers[i]} "

    return time_str if time_str != "" else "1 seconds"


async def validate_user(ctx: commands.Context) -> bool | None:
    """Check whether the user is registered with AniList account or not"""

    command_user = ctx.author
    data = await mongo_manager.manager.get_user(str(command_user.id))
    return data is not None


def short_cooldown():
    """Short Cooldown Decorator"""

    return commands.cooldown(rate=1, per=5, type=commands.BucketType.user)


def medium_cooldown():
    """Medium Cooldown Decorator! 5 requests per minute"""

    return commands.cooldown(rate=5, per=60, type=commands.BucketType.user)


def long_cooldown():
    return commands.cooldown(rate=2, per=5 * 60, type=commands.BucketType.user)


async def get_media_selection_paginator(
    media_name: str,
    select_callback: Callable[[], Awaitable[Paginator | Embed]],
    media_type="ANIME",
) -> DataInclusivePaginator:
    """Returns a list of medias to select from"""

    variables = {"search": media_name, "type": media_type}

    async with httpx.AsyncClient() as client:
        anime_resp = await client.post(
            url=config.ANILIST_BASE,
            json={"query": media_selection_query, "variables": variables},
        )

        anime_resp_json = json.loads(anime_resp.text)
        anime_data = anime_resp_json["data"]["Page"]["media"]

        pages = []
        media_list = []

        for page_data in anime_data:
            embd = Embed(
                title=f"Which {media_type} are you talking about?",
                color=config.NORMAL_COLOR,
            )

            embd.description = "**Name** : [{name}]({url})\n**Episodes** : {episodes}\n**Status** : {status}".format(
                name=(page_data["title"]["english"] if page_data["title"]["english"] is not None else page_data["title"]["romaji"]),
                url=page_data["siteUrl"],
                episodes=page_data["episodes"],
                status=page_data["status"],
            )

            genres = "\n".join([f"{config.BULLET_EMOTE}**{genre}**" for genre in page_data["genres"]]) if len(page_data["genres"]) > 0 else "<None>"
            embd.add_field(name="Genres", value=genres, inline=False)

            embd.set_thumbnail(url=page_data["coverImage"]["medium"])

            pages.append(embd)

            media_list.append(MediaData(page_data["id"], page_data["idMal"]))

    if len(pages) > 0:
        paginator = SelectPaginator(pages, select_callback)
    else:
        paginator = None

    return DataInclusivePaginator(paginator, media_list, media_type)


async def get_character_selection_paginator(character_name: str, select_callback: Callable[[], Awaitable[Embed]]) -> DataInclusivePaginator:
    """Returns a list of characters to select from"""

    variables = {"name": character_name}

    async with httpx.AsyncClient() as client:
        ch_response = await client.post(
            url=config.ANILIST_BASE,
            json={"query": character_selection_query, "variables": variables},
        )

        ch_response_raw = json.loads(ch_response.text)
        ch_data = ch_response_raw["data"]["Page"]["characters"]

        pages = []
        media_list = []

        for page_data in ch_data:
            embd = Embed(
                title="Which CHARACTER are you talking about?",
                color=config.NORMAL_COLOR,
            )

            embd.description = "**Name** : [{name}]({url}), {native}\n**Gender** : {gender}\n**Age** : {age}\n**Date Of Birth** : {dob}\n**Favorites** : {favorites}".format(
                name=page_data["name"]["full"],
                native=page_data["name"]["native"],
                url=page_data["siteUrl"],
                favorites=page_data["favourites"],
                age=page_data["age"],
                gender=page_data["gender"],
                dob="{d} {m}".format(
                    d=page_data["dateOfBirth"]["day"],
                    m=page_data["dateOfBirth"]["month"],
                ),
            )

            embd.set_thumbnail(url=page_data["image"]["medium"])

            pages.append(embd)
            media_list.append(CharacterData(page_data["id"]))

    if len(pages) > 0:
        paginator = SelectPaginator(pages, select_callback)
    else:
        paginator = None

    return DataInclusivePaginator(paginator, media_list, "CHARACTER")


async def encrypt_token(token: str) -> str:
    """Encrypts the token using the stored key"""

    cipher_suit = Fernet(config.SECRET_KEY)

    encrypted_token = cipher_suit.encrypt(token.encode())

    return encrypted_token.decode()


async def decrypt_token(encrypted_token: str) -> str:
    cipher_suit = Fernet(config.SECRET_KEY)

    decrypted_token = cipher_suit.decrypt(encrypted_token)

    return decrypted_token.decode()


def with_typing_msg():
    """Adds BOT is typing... to commands with message object"""

    def decorator(func):
        @wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            async with message.channel.typing():
                return await func(message, *args, **kwargs)

        return wrapper

    return decorator


def with_typing_ctx():
    """Adds BOT is typing... to commands with commands.Context object"""

    def decorator(func):
        @wraps(func)
        async def wrapper(self, ctx: commands.Context, *args, **kwargs):
            async with ctx.typing():
                return await func(self, ctx, *args, **kwargs)

        return wrapper

    return decorator


async def get_error_embed(data_raw: dict) -> Embed:
    """
    Get Error Embed from Anilist Response
    """
    errors = [error["message"] for error in data_raw["errors"]]
    return await general_helper.get_information_embed(
        title="Error Occurred!",
        color=config.ERROR_COLOR,
        description="{}{}".format(config.BULLET_EMOTE, f"\n{config.BULLET_EMOTE}".join(errors)),
    )
