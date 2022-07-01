from discord import Embed, Member
from datetime import datetime

from config import NORMAL_COLOR

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

    