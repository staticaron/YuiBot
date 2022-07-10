import requests
from discord import Embed, Member

from views.select_view import SelectPaginator
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