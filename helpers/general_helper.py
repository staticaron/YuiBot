from discord import Embed, Member
from datetime import datetime
import requests
import jwt

from managers import mongo_manager
from config import NORMAL_COLOR, ANILIST_BASE, ERROR_COLOR

"""Returns an embed with specified details"""

async def get_information_embed(title:str, color=NORMAL_COLOR, url:str=None, description:str=None, user:Member=None, thumbnail_link:str=None, fields:list=None) -> Embed:

    embd:Embed = Embed(title=title, color=color)
    embd.timestamp = datetime.now()

    if url is not None:
        embd.url = url

    if description is not None:
        embd.description = description

    if user is not None:
        embd.set_footer(icon_url=user.avatar.url, text="Requested by {}".format(user.name))

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

async def get_id_from_anilist_username(username:str) -> int:

    query = """
        query($username:String){
            User(search:$username){
                id
            }
        }
    """

    variables = {
        "username" : username
    }

    resp = requests.post(ANILIST_BASE, json={"query" : query, "variables" : variables})

    try:
        return resp.json()["data"]["User"]["id"]
    except Exception as e:
        print(e)
        return None

"""Returns the aniList Id from token"""

async def get_id_from_token(token:str) -> str:
    data = jwt.decode(token, options={"verify_signature": False})

    return data["sub"]

"""Returns the aniList id from userID"""

async def get_id_from_userID(userID:str) -> str:
    
    data = await mongo_manager.manager.get_user(userID)

    if data is not None:
        return data["anilistID"]
    else:
        return None

"""Returns a formatted time string"""

async def get_time_str_from_seconds(seconds:int):

    time_str = ""

    hours = seconds // 3600
    seconds = seconds - hours * 3600
    minutes = seconds // 60
    seconds = seconds - minutes * 60

    time_vals = (hours, minutes, seconds)
    time_markers = ("hours", "minutes", "seconds")

    for i in range(len(time_vals)):
        if time_vals[i] > 0:
            time_str += "{} {} ".format(time_vals[i], time_markers[i])

    return (time_str if time_str != "" else "0 seconds")

"""Check whether the user is registered with AniList account or not"""

async def validate_user(ctx:commands.Context):

    command_user = ctx.author

    data = await mongo_manager.manager.get_user(str(command_user.id))

    if data is None:
        return False

    return True