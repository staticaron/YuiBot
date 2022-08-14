from discord import Member, Embed
import requests

from managers import mongo_manager
from helpers import general_helper
from queries import user_query
import config

"""Check whether user is following the target on AniList"""

async def is_following(current_user_token:str, targetID:str) -> bool:

    # Check if already following the target or not.
    follow_check_query = """
        query($targetID:Int){
            User(id:$targetID){
                name
                siteUrl
                avatar{
                    medium
                }
                isFollowing
            }
        }
    """

    follow_check_variables = {
        "targetID" : targetID
    }

    follow_check_response = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query" : follow_check_query,
            "variables" : follow_check_variables
        },
        headers={
            "Authorization" : current_user_token
        }
    ).json()

    return follow_check_response["data"]["User"]["isFollowing"]

"""Get user information from AniList"""

async def get_user_embed(userID:str) -> Embed:
    
    data = await mongo_manager.manager.get_user(userID)

    anilistID = int(data["anilistID"])

    user_resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query" : user_query.user_query,
            "variables" : {"id" : anilistID}
        }
    ).json()

    user_data = user_resp["data"]["User"]
    social_data = user_resp["data"]["Page"]

    if user_data is None:
        pass

    embd:Embed = Embed(
        title="User Information",
        description="**Name** : [{name}]({url})\n**Followers** : {followers}".format(
            name=user_data["name"], 
            url=user_data["siteUrl"],
            followers=social_data["pageInfo"]["total"]
        ),
        color=config.NORMAL_COLOR
    )

    fav_anime = "\n".join(["[{name}]({url})".format(name=anime["title"]["english"] if anime["title"]["english"] is not None else anime["title"]["romaji"], url=anime["siteUrl"]) for anime in user_data["favourites"]["anime"]["nodes"]]) + " ..."
    fav_anime = ("None" if len(user_data["favourites"]["anime"]["nodes"]) <= 0 else fav_anime)

    embd.add_field(
        name="Favorite Anime",
        value=fav_anime,
        inline=True
    )

    fav_manga = "\n".join(["[{name}]({url})".format(name=manga["title"]["english"] if manga["title"]["english"] is not None else manga["title"]["romaji"], url=manga["siteUrl"]) for manga in user_data["favourites"]["manga"]["nodes"]]) + " ..."
    fav_manga = ("None" if len(user_data["favourites"]["manga"]["nodes"]) <= 0 else fav_manga)

    embd.add_field(
        name="Favorite Manga",
        value=fav_manga,
        inline=True
    )

    fav_characters = "\n".join(["[{name}]({url})".format(name=character["name"]["full"], url=character["siteUrl"]) for character in user_data["favourites"]["characters"]["nodes"]]) + " ..."
    fav_characters = ("None" if len(user_data["favourites"]["characters"]["nodes"]) <= 0 else fav_characters)

    embd.add_field(
        name="Favorite Characters",
        value=fav_characters,
        inline=True
    )

    embd.add_field(
        name="Anime Stats",
        value="Count : **{count}**\nMean Score : **{mean_score}**\nStandard Deviation : **{standard_deviation}**\nEpisode Watched : **{episodes}**\nTop Genre : \n{genre}".format(
            count=user_data["statistics"]["anime"]["count"],
            mean_score=user_data["statistics"]["anime"]["meanScore"],
            standard_deviation=user_data["statistics"]["anime"]["standardDeviation"],
            episodes=user_data["statistics"]["anime"]["episodesWatched"],
            genre="\n".join("{bullet}**{name}**".format(name=genre["genre"], bullet=config.BULLET_EMOTE) for genre in user_data["statistics"]["anime"]["genres"])
        ),
        inline=True
    )

    embd.add_field(
        name="Manga Stats",
        value="Count : **{count}**\nMean Score : **{mean_score}**\nStandard Deviation : **{standard_deviation}**\nChapters Read : **{chapters}**\nTop Genre : \n{genre}".format(
            count=user_data["statistics"]["manga"]["count"],
            mean_score=user_data["statistics"]["manga"]["meanScore"],
            standard_deviation=user_data["statistics"]["manga"]["standardDeviation"],
            chapters=user_data["statistics"]["manga"]["chaptersRead"],
            genre="\n".join("{bullet}**{name}**".format(name=genre["genre"], bullet=config.BULLET_EMOTE) for genre in user_data["statistics"]["manga"]["genres"])
        ),
        inline=True
    )

    embd.set_thumbnail(url=user_data["avatar"]["medium"])

    return embd

"""Follow a discord user on AniList"""

async def follow_user(user:Member, target:Member) -> Embed:

    # Get the target's anilist ID
    target_data = await mongo_manager.manager.get_user(str(target.id))

    if target_data is None:
        return await general_helper.get_information_embed(
            title="Hold It",
            description="<@{}> has not linked his account yet. Ask them to link their AniList account using `login` command.".format(target.id),
            color=config.ERROR_COLOR
        )

    target_anilistID = target_data["anilistID"]

    # Get the current user's token
    current_user = await mongo_manager.manager.get_user(str(user.id))
    current_user_token = current_user["token"]

    is_already_following = await is_following(current_user_token, target_anilistID)

    if is_already_following:
        return await general_helper.get_information_embed(
            title="Hold It",
            color=config.INFO_COLOR,
            description="You are already following <@{}>".format(target.id)
        )

    # add the target to the follow list.

    follow_query = """
        mutation($targetID:Int){
            ToggleFollow(userId:$targetID){
                name
                siteUrl
                avatar{
                    medium
                }
            }
        }
    """

    variables = {
        "targetID" : target_anilistID
    }

    follow_response = requests.post(url=config.ANILIST_BASE, json={
        "query" : follow_query,
        "variables" : variables
    }, headers={
        "Authorization" : current_user_token
    })

    follow_response = follow_response.json()

    if follow_response["data"]["ToggleFollow"] is None:

        errors = [error["message"] for error in follow_response["errors"]]

        return await general_helper.get_information_embed(
            title="Error Occurred!",
            color=config.ERROR_COLOR,
            description="The following error occurred : ```>{}```".format(f"\n>".join(errors))
        )

    return (await general_helper.get_information_embed(
        title="Done",
        description="You are now following [{name}]({url})".format(name=follow_response["data"]["ToggleFollow"]["name"], url=follow_response["data"]["ToggleFollow"]["siteUrl"])
    )).set_thumbnail(url=follow_response["data"]["ToggleFollow"]["avatar"]["medium"])

"""Unfollow a discord user on AniList"""

async def unfollow_user(user:Member, target:Member) -> Embed:

    # Get the target's anilist ID
    target_data = await mongo_manager.manager.get_user(str(target.id))
    target_anilistID = target_data["anilistID"]

    # Get the current user's token
    current_user = await mongo_manager.manager.get_user(str(user.id))
    current_user_token = current_user["token"]

    is_already_following = await is_following(current_user_token, target_anilistID)

    if not is_already_following:
        return await general_helper.get_information_embed(
            title="Hold It",
            color=config.INFO_COLOR,
            description="You are not even following <@{}>".format(target.id)
        )

    # remove the target from the follow list.

    follow_query = """
        mutation($targetID:Int){
            ToggleFollow(userId:$targetID){
                name
                siteUrl
                avatar{
                    medium
                }
            }
        }
    """

    variables = {
        "targetID" : target_anilistID
    }

    unfollow_response = requests.post(url=config.ANILIST_BASE, json={
        "query" : follow_query,
        "variables" : variables
    }, headers={
        "Authorization" : current_user_token
    })

    unfollow_response = unfollow_response.json()

    if unfollow_response["data"]["ToggleFollow"] is None:

        errors = [error["message"] for error in unfollow_response["errors"]]

        return await general_helper.get_information_embed(
            title="Error Occurred!",
            color=config.ERROR_COLOR,
            description="The following error occurred : ```>{}```".format(f"\n>".join(errors))
        )

    return (await general_helper.get_information_embed(
        title="Done",
        description="You are no longer following [{name}]({url})".format(name=unfollow_response["data"]["ToggleFollow"]["name"], url=unfollow_response["data"]["ToggleFollow"]["siteUrl"])
    )).set_thumbnail(url=unfollow_response["data"]["ToggleFollow"]["avatar"]["medium"])

"""Get user media stats """

async def get_user_media_stats(target:Member, media_type:str="ANIME") -> Embed:

    if media_type == "ANIME":
        stats_query = user_query.anime_stats_query
    elif media_type == "MANGA":
        stats_query = user_query.manga_stats_query

    anilistID = await general_helper.get_id_from_userID(str(target.id))

    stats_resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query" : stats_query,
            "variables" : {
                "userID" : anilistID
            }
        }
    ).json()

    user_data = stats_resp["data"]["User"]
    if media_type == "ANIME":
        stats_data = stats_resp["data"]["User"]["statistics"]["anime"]
    else:
        stats_data = stats_resp["data"]["User"]["statistics"]["manga"]

    embd = Embed(
        title="Anime Statistics",
        description="**Name : ** [{}]({})\n\n".format(user_data["name"], user_data["siteUrl"])
    )

    embd.set_thumbnail(url=user_data["avatar"]["medium"])

    embd.add_field(
        name="Total Count",
        value=str(stats_data["count"]),
        inline=False
    )

    embd.add_field(
        name="Mean Score",
        value=str(stats_data["meanScore"]),
        inline=False
    )

    if media_type == "ANIME":
        embd.add_field(
            name="Standard Deviation",
            value=str(stats_data["standardDeviation"]),
            inline=False
        )

    if media_type == "ANIME":
        embd.add_field(
            name="Episodes Watched",
            value=str(stats_data["episodesWatched"]),
            inline=False
        )
    else:
        embd.add_field(
            name="Chapters Read",
            value=str(stats_data["chaptersRead"]),
            inline=False
        )

    if media_type == "ANIME":
        embd.add_field(
            name="Watch Time",
            value=await general_helper.get_time_str_from_seconds(stats_data["minutesWatched"] * 60, 2),
            inline=False
        )

    if media_type == "MANGA":
        embd.add_field(
            name="Volumes Read",
            value=str(stats_data["volumesRead"]),
            inline=False
        )

    return embd