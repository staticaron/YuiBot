import json

import httpx
from discord import Embed

import config
from helpers import general_helper
from managers import mongo_manager
from queries.media_queries import (
    media_rate_query,
    progress_query,
    progress_update_query,
)
from utils.errors.UserNotFound import UserNotFound
from views.scroller import Scroller


async def set_progress(userID: str, mediaID: int, progress: int) -> Embed:

    anilist_user = await mongo_manager.manager.get_user(userID)
    if anilist_user is None:
        raise UserNotFound(None, userID)

    if progress == -1:
        async with httpx.AsyncClient() as client:
            progress_resp = await client.post(
                url=config.ANILIST_BASE,
                json={"query": progress_query, "variables": {"mediaID": mediaID}},
                headers={"Authorization": anilist_user["token"]},
            )

        progress_resp_raw = json.loads(progress_resp.text)
        data = progress_resp_raw["data"]["Media"]["mediaListEntry"]

        progress = data["progress"] + 1

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url=config.ANILIST_BASE,
            json={
                "query": progress_update_query,
                "variables": {"mediaID": mediaID, "progress": progress},
            },
            headers={"Authorization": anilist_user["token"]},
        )

        resp_json = json.loads(resp.text)
        data = resp_json["data"]["SaveMediaListEntry"]

        title = (
            data["media"]["title"]["english"]
            if data["media"]["title"]["english"] is not None
            else data["media"]["title"]["native"]
        )

        return await general_helper.get_information_embed(
            title="Done", description=f"Progress of `{title}` was set to **{progress}**"
        )


async def rate_media(
    userID: str, media_id: int, rating: float, media_type: str = "ANIME"
):

    anilist_user = await mongo_manager.manager.get_user(userID)
    if anilist_user is None:
        raise UserNotFound(None, userID)

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url=config.ANILIST_BASE,
            json={
                "query": media_rate_query,
                "variables": {"mediaID": media_id, "rating": rating},
            },
            headers={"Authorization": anilist_user["token"]},
        )

        resp_json = json.loads(resp.text)
        saved_media_list_data = resp_json["data"]["SaveMediaListEntry"]

        if saved_media_list_data is None:
            return (
                await general_helper.get_information_embed(
                    title="Whoops",
                    description="Error occurred while trying to run this command!",
                    color=config.ERROR_COLOR,
                )
            ).add_field(
                name="Details for nerds",
                value="```"
                + "\n".join([error["message"] for error in resp_json["data"]["errors"]])
                + "```",
            )

        title = (
            saved_media_list_data["media"]["title"]["english"]
            if saved_media_list_data["media"]["title"]["english"] is not None
            else saved_media_list_data["media"]["title"]["native"]
        )

        return await general_helper.get_information_embed(
            title="Done", description=f"`{title}` is now rated at **{rating}**"
        )


async def get_watch_order_embd(malID: int, anime: str) -> Scroller:

    MAX_PER_PAGE = 10

    async with httpx.AsyncClient() as client:
        resp = await client.get(config.CHIAKI_BASE.format(malID))
        resp_json = json.loads(resp.text)

        embds = []
        current_count = 0

        embd = await general_helper.get_information_embed(
            title=f"{anime.title()}'s watch order",
            description="Anime that appear on top are to be watched first.",
        )

        for data_element in resp_json:
            current_count += 1

            embd.add_field(
                name=data_element["index"],
                value="Name : **{}**\nInfo : {}\n [MAL]({})".format(
                    data_element["name"], data_element["info"], data_element["url"]
                ),
                inline=False,
            )

            if current_count >= MAX_PER_PAGE:
                embds.append(embd)
                embd = await general_helper.get_information_embed(
                    title=f"{anime.title()}'s watch order",
                    description="Anime that appear on top are to be watched first.",
                )
                current_count = 0

        embds.append(embd)

        return Scroller(embds, True)
