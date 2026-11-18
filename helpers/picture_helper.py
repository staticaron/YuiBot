import json
import random

import httpx
from discord import Embed, Member, User

import config
from helpers import general_helper

reactions_single = {
    "cry": ["cry", "{user} is crying"],
    "sob": ["cry", "{user} is sobbing"],
    "wave": ["wave", "{user} is waving"],
    "hi": ["wave", "{user} is waving"],
    "smug": ["smug", "{user} is smugging"],
    "happy": ["happy", "{user} is happy"],
    "nom": ["nom", "nom nom {user} "],
    "wink": ["wink", "{user} winked"],
    "dance": ["dance", "{user} is dancing like a pro"],
    "lurk": ["lurk", "{user} is lurking"],
    "shoot": ["shoot", "{user} is shooting"],
    "sleep": ["sleep", "{user} is sleeping"],
    "shrug": ["shrug", "{user} is shrugging"],
    "stare": ["stare", "{user} is staring"],
    "sip": ["sip", "{user} is sipping"],
    "blush": ["blush", "{user} is blushing"],
    "think": ["think", "{user} is thinking"],
}

reactions_double = {
    "slap": ["slap", "{user} slapped {target}"],
    "kick": ["kick", "{user} kicked {target}"],
    "cuddle": ["cuddle", "{user} cuddles {target}"],
    "kiss": ["kiss", "{user} kissed {target} :O"],
    "hug": ["hug", "{user} hugs {target} :}"],
    "pat": ["pat", "{user} pets {target}"],
    "bite": ["bite", "{user} bit {target}"],
    "bonk": ["bonk", "{user} bonked {target}"],
    "poke": ["poke", "{user} poked {target}"],
}


async def fetch_waifu_api(endpoint: str | None = None) -> str:

    if endpoint is None:
        endpoint = "waifu" if random.randint(0, 100) > 30 else "neko"

    url = f"https://nekos.best/api/v2/{endpoint}"

    async with httpx.AsyncClient() as client:
        waifu_resp = await client.get(url)

    waifu_resp_json = json.loads(waifu_resp.text)

    if len(waifu_resp_json.get("results")) <= 0:
        return ""

    top_match = waifu_resp_json.get("results")[0].get("url", "")
    return top_match


async def get_waifu_embed():

    embd = Embed(title="Waifu Picture")

    url = await fetch_waifu_api()
    embd.set_image(url=url)

    return embd


async def get_reaction_embed(reaction: str, user: User | Member, target: Member | User | None):

    reaction = reaction.lower()

    is_double = reaction in reactions_double
    is_single = reaction in reactions_single

    if not (is_single or is_double):
        return await general_helper.get_information_embed(
            title="Not Found",
            description="This reaction type was not found.\nValid Reactions include : \n\n**Single** : `{}`\n\n**Pair** : `{}`".format(
                " ,".join(list(reactions_single.keys())),
                " ,".join(reactions_double.keys()),
            ),
            color=config.ERROR_COLOR,
        )

    endpoint = None
    title = None

    if is_single:
        endpoint = reactions_single[reaction][0]
        title = reactions_single[reaction][1].format(user=user.name)
    else:
        if target is None:
            return await general_helper.get_information_embed("Error!", description="Please provide a target user by tagging them! For example @yuibot gif slap @user", color=config.ERROR_COLOR)

        endpoint = reactions_double[reaction][0]
        title = reactions_double[reaction][1].format(user=user.name, target=target.name)

    url = await fetch_waifu_api(endpoint)

    embd = Embed(title=title, color=config.NORMAL_COLOR).set_image(url=url)
    print("URL : ", url)

    return embd
