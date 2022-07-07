from discord import Member
import requests

from managers import mongo_manager
from helpers import general_helper
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

"""Follow a discord user on AniList"""

async def follow_user(user:Member, target:Member) -> str:

    # Get the target's anilist ID
    target_data = await mongo_manager.manager.get_user(str(target.id))
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

    # Reusing the variables from follow_check_response and not pulling them again from the API

    return (await general_helper.get_information_embed(
        title="Done",
        description="You are now following [{name}]({url})".format(name=follow_response["data"]["ToggleFollow"]["name"], url=follow_response["data"]["ToggleFollow"]["siteUrl"])
    )).set_thumbnail(url=follow_response["data"]["ToggleFollow"]["avatar"]["medium"])

"""Unfollow a discord user on AniList"""

async def unfollow_user(user:Member, target:Member) -> str:

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

    # Reusing the variables from follow_check_response and not pulling them again from the API

    return (await general_helper.get_information_embed(
        title="Done",
        description="You are no longer following [{name}]({url})".format(name=follow_response["data"]["ToggleFollow"]["name"], url=follow_response["data"]["ToggleFollow"]["siteUrl"])
    )).set_thumbnail(url=follow_response["data"]["ToggleFollow"]["avatar"]["medium"])



