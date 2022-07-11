import requests
from discord import Embed, Member

from views.scroller import Scroller
from managers import mongo_manager
from helpers import general_helper
import config

all_lists = ["ptw", "planning", "crt", "current", "watching", "comp", "completed", "drp", "dropped"]

lists = {
    "ptw" : "PLANNING",
    "planning" : "PLANNING",
    "crt" : "CURRENT",
    "current" : "CURRENT",
    "watching" : "CURRENT",
    "comp" : "COMPLETED",
    "completed" : "COMPLETED",
    "drp" : "DROPPED",
    "dropped" : "DROPPED"
}

"""Adds specified anime to the specified list"""

async def add_to_list(list_name:str, mediaID:int, user:Member) -> Embed:

    lst = lists[list_name]

    list_query = """
        mutation($id:Int!, $list:MediaListStatus){
            SaveMediaListEntry(mediaId:$id, status:$list){
                id 
                status
            }
        }
    """

    token = (await mongo_manager.manager.get_user(str(user.id)))["token"]

    list_resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query" : list_query,
            "variables" : {
                "id" : mediaID,
                "list" : lst
            }
        },
        headers={
            "Authorization" : token
        }
    ).json()    
    
    if list_resp["data"]["SaveMediaListEntry"] is None:
        return await general_helper.get_information_embed(
            title="Whoops",
            description="The following error occurred : ```{}```".format(list_resp["error"]["message"]),
            color=config.ERROR_COLOR
        )

    return await general_helper.get_information_embed(
        title="Done",
        description="Anime was added to your `{}` list.".format(lst)
    )

async def get_list_paginator(target:Member, list_name:str):

    anilistID = await general_helper.get_id_from_userID(str(target.id))

    list_query = """
        query($id:Int!, $status:MediaListStatus){
            MediaListCollection(userId:$id, type:ANIME, status:$status, sort:UPDATED_TIME_DESC){
                lists{
                    name
                    entries{
                        media{
                            title{
                                english
                                romaji
                            }
                            siteUrl
                            episodes
                        }
                        progress
                    }
                    isCustomList
                }
            }
        }
    """

    list_resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query" : list_query,
            "variables" : {
                "id" : anilistID,
                "status" : list_name
            }
        }
    ).json()

    list_data = None

    for i in list_resp["data"]["MediaListCollection"]["lists"]:
        if i["isCustomList"] is False:
            list_data = i

    if list_data is None:
        return None

    entries = list_data["entries"]

    pages = []

    MAX_LISTINGS_PER_PAGE = 10
    current_listing_count = 0

    current_embed = Embed(
        title=list_data["name"] + " list",
        description="Total : {}\n\n".format(len(entries))
    )
    
    for i in range(len(entries)):

        current_listing_count += 1

        if current_listing_count > MAX_LISTINGS_PER_PAGE:
            current_listing_count = 1
            pages.append(current_embed)
            current_embed = Embed(
                title=list_data["name"] + " list",
                description="Total : {}\n\n".format(len(entries))
            )

        current_title = (entries[i]["media"]["title"]["english"] if entries[i]["media"]["title"]["english"] is not None else entries[i]["media"]["title"]["romaji"])
        current_embed.description += "{bullet} [{name}]({url}) {progress}/{episodes}\n".format(
            bullet=config.BULLET_EMOTE,
            name=current_title,
            url=entries[i]["media"]["siteUrl"],
            progress=entries[i]["progress"],
            episodes=entries[i]["media"]["episodes"]
        )

        if i >= len(entries) - 1:
            pages.append(current_embed)

    if len(pages) > 0:
        return Scroller(pages, True)
    else:
        return None

    

    