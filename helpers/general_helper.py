from discord import Embed, Member
from discord.ext import commands
from datetime import datetime
import requests
import jwt

from managers import mongo_manager
from config import NORMAL_COLOR, ANILIST_BASE, ERROR_COLOR

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

async def get_id_from_token(token:str) -> str:
    data = jwt.decode(token, options={"verify_signature": False})

    return data["sub"]

async def get_id_from_userID(userID:str) -> str:
    
    data = await mongo_manager.manager.get_user(userID)

    if data is not None:
        return data["anilistID"]
    else:
        return None

"""Check whether the user is registered with AniList account or not"""

def validate_user(func):

    async def predicate(user_class, ctx, *args, **kwargs):

        command_user = ctx.author

        data = await mongo_manager.manager.get_user(str(command_user.id))

        if data is None:
            reply = await get_information_embed(
                title="Hold It",
                description="Log-In with your AniList account before using that command.\nUse `login` command to login.",
                color=ERROR_COLOR
            )
            return await ctx.reply(embed=reply)

        print(args)
        print(kwargs)

        await func(user_class, ctx, *args, **kwargs)

    return predicate