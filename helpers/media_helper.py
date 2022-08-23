from discord import Embed
import requests

from views.scroller import Scroller
from managers import mongo_manager
from helpers import general_helper
from queries.media_queries import progress_query, progress_update_query, media_rate_query
import config


async def set_progress(userID: str, mediaID: int, progress: int) -> Embed:

    anilist_user = await mongo_manager.manager.get_user(userID)

    if progress == -1:
        progress_resp = requests.post(
            url=config.ANILIST_BASE,
            json={
                "query" : progress_query,
                "variables" : {
                    "mediaID" : mediaID
                }
            },
            headers={
                "Authorization" : anilist_user["token"]
            }
        ).json()

        data = progress_resp["data"]["Media"]["mediaListEntry"]

        progress = data["progress"] + 1

    resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query": progress_update_query,
            "variables": {
                "mediaID": mediaID,
                "progress": progress
            }
        },
        headers={
            "Authorization": anilist_user["token"]
        }).json()

    data = resp["data"]["SaveMediaListEntry"]

    title = (data["media"]["title"]["english"] if data["media"]["title"]
             ["english"] is not None else data["media"]["title"]["native"])

    return await general_helper.get_information_embed(
        title="Done",
        description="Progress of `{}` was set to **{}**".format(
            title, progress
        )
    )


async def rate_media(userID: str, media_id: int, rating: float, media_type: str = "ANIME"):

    anilist_user = await mongo_manager.manager.get_user(userID)

    resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query": media_rate_query,
            "variables": {
                "mediaID": media_id,
                "rating": rating
            }
        },
        headers={
            "Authorization": anilist_user["token"]
        }
    ).json()

    data = resp["data"]["SaveMediaListEntry"]

    if data is None:
        return (await general_helper.get_information_embed(
            title="Whoops",
            description="Error occurred while trying to run this command!",
            color=config.ERROR_COLOR
        )).add_field(
            name="Details for nerds",
            value="```" + "\n".join([error["message"]
                                    for error in data["errors"]]) + "```"
        )

    title = (data["media"]["title"]["english"] if data["media"]["title"]
             ["english"] is not None else data["media"]["title"]["native"])

    return await general_helper.get_information_embed(
        title="Done",
        description="`{}` is now rated at **{}**".format(title, rating)
    )


async def get_watch_order_embd(malID: int, anime: str) -> Scroller:

    MAX_PER_PAGE = 10

    resp = requests.get(config.CHIAKI_BASE.format(malID)).json()

    embds = []
    current_count = 0

    embd = (await general_helper.get_information_embed(title="{}'s watch order".format(anime.capitalize()), description="Anime that appear on top are to be watched first."))

    for data_element in resp:

        current_count += 1

        embd.add_field(
            name=data_element["index"],
            value="Name : **{}**\nInfo : {}\n [MAL]({})".format(
                data_element["name"], data_element["info"], data_element["url"]),
            inline=False
        )

        if current_count >= MAX_PER_PAGE:
            embds.append(embd)
            embd = (await general_helper.get_information_embed(title="{}'s watch order".format(anime.capitalize()), description="Anime that appear on top are to be watched first."))
            current_count = 0

    embds.append(embd)

    return Scroller(embds, True)
