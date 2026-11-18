import json

import httpx
from discord import Embed, Member, User

import config
from helpers import general_helper
from managers import mongo_manager
from queries.user_query import *
from utils.errors.UserNotFound import UserNotFound

"""Check whether user is following the target on AniList"""


async def is_following(current_user_token: str, targetID: str) -> bool:
    # Check if already following the target or not.

    follow_check_variables = {"targetID": targetID}

    async with httpx.AsyncClient() as client:
        follow_check_response_raw = await client.post(
            url=config.ANILIST_BASE,
            json={"query": follow_check_query, "variables": follow_check_variables},
            headers={"Authorization": current_user_token},
        )

    follow_check_response = json.loads(follow_check_response_raw.text)
    return follow_check_response["data"]["User"]["isFollowing"]


"""Get user information from AniList"""


async def get_user_embed(targetID: str, user: User | Member | None = None) -> Embed:
    target_user = await mongo_manager.manager.get_user(targetID)
    if target_user is None:
        raise UserNotFound(user_id=targetID)

    anilistID = int(target_user["anilistID"])
    current_user = await mongo_manager.manager.get_user(str(user.id)) if user is not None else None

    if current_user is not None:
        async with httpx.AsyncClient() as client:
            user_resp_raw = await client.post(
                url=config.ANILIST_BASE,
                json={"query": user_query, "variables": {"id": anilistID}},
                headers={"Authorization": current_user["token"]},
            )

    # Fetch without any token
    else:
        async with httpx.AsyncClient() as client:
            user_resp_raw = await client.post(
                url=config.ANILIST_BASE,
                json={"query": user_query, "variables": {"id": anilistID}},
            )

    user_resp = json.loads(user_resp_raw.text)

    user_data: dict | None = user_resp["data"]["User"]
    social_data: dict = user_resp["data"]["Page"]

    if user_data is None:
        raise UserNotFound(None, targetID)

    embd: Embed = Embed(
        title="User Information",
        description="**Name** : [{name}]({url})\n**Followers** : {followers}".format(
            name=user_data["name"],
            url=user_data["siteUrl"],
            followers=social_data.get("pageInfo", {}).get("total", "-"),
        ),
        color=config.NORMAL_COLOR,
    )

    fav_anime = (
        "\n".join(
            [
                "[{name}]({url})".format(
                    name=anime["title"]["english"] if anime["title"]["english"] is not None else anime["title"]["romaji"],
                    url=anime["siteUrl"],
                )
                for anime in user_data["favourites"]["anime"]["nodes"]
            ]
        )
        + " ..."
    )
    fav_anime = "None" if len(user_data["favourites"]["anime"]["nodes"]) <= 0 else fav_anime

    embd.add_field(name="Favorite Anime", value=fav_anime, inline=True)

    fav_manga = (
        "\n".join(
            [
                "[{name}]({url})".format(
                    name=manga["title"]["english"] if manga["title"]["english"] is not None else manga["title"]["romaji"],
                    url=manga["siteUrl"],
                )
                for manga in user_data["favourites"]["manga"]["nodes"]
            ]
        )
        + " ..."
    )
    fav_manga = "None" if len(user_data["favourites"]["manga"]["nodes"]) <= 0 else fav_manga

    embd.add_field(name="Favorite Manga", value=fav_manga, inline=True)

    fav_characters = "\n".join(["[{name}]({url})".format(name=character["name"]["full"], url=character["siteUrl"]) for character in user_data["favourites"]["characters"]["nodes"]]) + " ..."
    fav_characters = "None" if len(user_data["favourites"]["characters"]["nodes"]) <= 0 else fav_characters

    embd.add_field(name="Favorite Characters", value=fav_characters, inline=True)

    embd.add_field(
        name="Anime Stats",
        value="Count : **{count}**\nMean Score : **{mean_score}**\nStandard Deviation : **{standard_deviation}**\nEpisode Watched : **{episodes}**\nTop Genre : \n{genre}".format(
            count=user_data["statistics"]["anime"]["count"],
            mean_score=user_data["statistics"]["anime"]["meanScore"],
            standard_deviation=user_data["statistics"]["anime"]["standardDeviation"],
            episodes=user_data["statistics"]["anime"]["episodesWatched"],
            genre="\n".join("{bullet}**{name}**".format(name=genre["genre"], bullet=config.BULLET_EMOTE) for genre in user_data["statistics"]["anime"]["genres"]),
        ),
        inline=True,
    )

    embd.add_field(
        name="Manga Stats",
        value="Count : **{count}**\nMean Score : **{mean_score}**\nStandard Deviation : **{standard_deviation}**\nChapters Read : **{chapters}**\nTop Genre : \n{genre}".format(
            count=user_data["statistics"]["manga"]["count"],
            mean_score=user_data["statistics"]["manga"]["meanScore"],
            standard_deviation=user_data["statistics"]["manga"]["standardDeviation"],
            chapters=user_data["statistics"]["manga"]["chaptersRead"],
            genre="\n".join("{bullet}**{name}**".format(name=genre["genre"], bullet=config.BULLET_EMOTE) for genre in user_data["statistics"]["manga"]["genres"]),
        ),
        inline=True,
    )

    embd.set_thumbnail(url=user_data["avatar"]["medium"])

    return embd


"""Follow a discord user on AniList"""


async def follow_user(user: User | Member, target: Member) -> Embed:

    # Get the target's anilist ID
    target_data = await mongo_manager.manager.get_user(str(target.id))
    if target_data is None:
        raise UserNotFound(target, None)

    target_anilistID = target_data["anilistID"]

    # Get the current user's token
    current_user = await mongo_manager.manager.get_user(str(user.id))
    if current_user is None:
        raise UserNotFound(user, None)

    current_user_token = current_user["token"]

    is_already_following = await is_following(current_user_token, target_anilistID)

    if is_already_following:
        return await general_helper.get_information_embed(
            title="Hold It",
            color=config.INFO_COLOR,
            description=f"You are already following <@{target.id}>",
        )

    # add the target to the follow list.

    variables = {"targetID": target_anilistID}

    async with httpx.AsyncClient() as client:
        follow_response_raw = await client.post(
            url=config.ANILIST_BASE,
            json={"query": follow_query, "variables": variables},
            headers={"Authorization": current_user_token},
        )

    follow_response = json.loads(follow_response_raw.text)

    if follow_response["data"]["ToggleFollow"] is None:
        errors = [error["message"] for error in follow_response["errors"]]

        return await general_helper.get_information_embed(
            title="Error Occurred!",
            color=config.ERROR_COLOR,
            description="The following error occurred : ```>{}```".format("\n>".join(errors)),
        )

    return (
        await general_helper.get_information_embed(
            title="Done",
            description="You are now following [{name}]({url})".format(
                name=follow_response["data"]["ToggleFollow"]["name"],
                url=follow_response["data"]["ToggleFollow"]["siteUrl"],
            ),
        )
    ).set_thumbnail(url=follow_response["data"]["ToggleFollow"]["avatar"]["medium"])


"""Unfollow a discord user on AniList"""


async def unfollow_user(user: User | Member, target: Member) -> Embed:
    # Get the target's anilist ID
    target_user = await mongo_manager.manager.get_user(str(target.id))
    if target_user is None:
        raise UserNotFound(user=target)

    target_anilistID = target_user["anilistID"]

    # Get the current user's token
    current_user = await mongo_manager.manager.get_user(str(user.id))
    if current_user is None:
        raise UserNotFound(user=user)

    current_user_token = current_user["token"]

    is_already_following = await is_following(current_user_token, target_anilistID)

    if not is_already_following:
        return await general_helper.get_information_embed(
            title="Hold It",
            color=config.INFO_COLOR,
            description=f"You are not even following <@{target.id}>",
        )

    variables = {"targetID": target_anilistID}

    async with httpx.AsyncClient() as client:
        unfollow_response_raw = await client.post(
            url=config.ANILIST_BASE,
            json={"query": follow_query, "variables": variables},
            headers={"Authorization": current_user_token},
        )

    unfollow_response = json.loads(unfollow_response_raw.text)

    if unfollow_response["data"]["ToggleFollow"] is None:
        errors = [error["message"] for error in unfollow_response["errors"]]

        return await general_helper.get_information_embed(
            title="Error Occurred!",
            color=config.ERROR_COLOR,
            description="The following error occurred : ```>{}```".format("\n>".join(errors)),
        )

    return (
        await general_helper.get_information_embed(
            title="Done",
            description="You are no longer following [{name}]({url})".format(
                name=unfollow_response["data"]["ToggleFollow"]["name"],
                url=unfollow_response["data"]["ToggleFollow"]["siteUrl"],
            ),
        )
    ).set_thumbnail(url=unfollow_response["data"]["ToggleFollow"]["avatar"]["medium"])


"""Get user media stats """


async def get_user_media_stats(target: User | Member, media_type: str = "ANIME") -> Embed:

    stats_query = anime_stats_query
    if media_type == "MANGA":
        stats_query = manga_stats_query

    anilistID = await general_helper.get_id_from_userID(str(target.id))

    async with httpx.AsyncClient() as client:
        stats_resp_raw = await client.post(
            url=config.ANILIST_BASE,
            json={"query": stats_query, "variables": {"userID": anilistID}},
        )

    stats_resp = json.loads(stats_resp_raw.text)

    user_data = stats_resp["data"]["User"]
    if media_type == "ANIME":
        stats_data = stats_resp["data"]["User"]["statistics"]["anime"]
    else:
        stats_data = stats_resp["data"]["User"]["statistics"]["manga"]

    embd = Embed(
        title="Anime Statistics",
        description="**Name : ** [{}]({})\n\n".format(user_data["name"], user_data["siteUrl"]),
    )

    embd.set_thumbnail(url=user_data["avatar"]["medium"])

    embd.add_field(name="Total Count", value=str(stats_data["count"]), inline=False)

    embd.add_field(name="Mean Score", value=str(stats_data["meanScore"]), inline=False)

    if media_type == "ANIME":
        embd.add_field(
            name="Standard Deviation",
            value=str(stats_data["standardDeviation"]),
            inline=False,
        )

    if media_type == "ANIME":
        embd.add_field(
            name="Episodes Watched",
            value=str(stats_data["episodesWatched"]),
            inline=False,
        )
    else:
        embd.add_field(name="Chapters Read", value=str(stats_data["chaptersRead"]), inline=False)

    if media_type == "ANIME":
        embd.add_field(
            name="Watch Time",
            value=await general_helper.get_time_str_from_seconds(stats_data["minutesWatched"] * 60, 2),
            inline=False,
        )

    if media_type == "MANGA":
        embd.add_field(name="Volumes Read", value=str(stats_data["volumesRead"]), inline=False)

    return embd
