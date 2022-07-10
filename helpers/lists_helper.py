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

"""Just a way to transmit paginator and ids at the same time. Please no bully"""

class AnimePaginator:
    paginator:SelectPaginator = None
    ids:list = None

    def __init__(self, paginator, ids):
        self.paginator = paginator
        self.ids = ids

"""Returns a list of anime to select from"""

async def get_anime_selection_paginator(anime:str, select_callback:callable) -> AnimePaginator:

    anime_query = """
        query($search:String){
            Page(page:0, perPage:5){
                pageInfo{
                    total
                }
                media(search:$search, sort:SEARCH_MATCH, type:ANIME){
                    id 
                    title{
                        english
                        romaji
                    }
                    siteUrl
                    genres
                    coverImage{
                        medium
                    }
                    episodes
                    status
                }
            }
        }
    """

    variables = {
        "search" : anime
    }

    anime_resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query" : anime_query,
            "variables" : variables
        }
    ).json()

    anime_data = anime_resp["data"]["Page"]["media"]

    pages = []
    ids = []

    for page_data in anime_data:
        embd = Embed(
            title=(page_data["title"]["english"] if page_data["title"]["english"] is not None else page_data["title"]["romaji"]),
            color=config.NORMAL_COLOR,
            url=page_data["siteUrl"]
        )

        embd.description = "**Genre** : {genre}\n**Episodes** : {episodes}\n**Status** : {status}".format(
            genre="\n" + "\n".join(["{bullet}**{genre}**".format(bullet=config.BULLET_EMOTE, genre=genre) for genre in page_data["genres"]]),
            episodes=page_data["episodes"],
            status=page_data["status"]
        )

        embd.set_thumbnail(url=page_data["coverImage"]["medium"])

        pages.append(embd)
        ids.append(page_data["id"])

    paginator = SelectPaginator(pages, select_callback)

    return AnimePaginator(paginator, ids)

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