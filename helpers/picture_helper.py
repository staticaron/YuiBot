import json
import random

import httpx
from discord import Embed, Member, User

import config
from helpers import general_helper

all_single_reactions = [
    "cry",
    "sob",
    "wave",
    "hi",
    "smug",
    "nom",
    "wink",
    "cringe",
    "dance",
    "happy",
]
all_double_reactions = [
    "kill",
    "bite",
    "slap",
    "kick",
    "cuddle",
    "hug",
    "pat",
    "bully",
    "harass",
    "lick",
    "bonk",
    "poke",
    "kiss",
]

reactions_single = {
    "cry": ["cry", "{user} is crying"],
    "sob": ["cry", "{user} is sobbing"],
    "wave": ["wave", "{user} is waving"],
    "hi": ["wave", "{user} is waving"],
    "smug": ["smug", "{user} is smugging"],
    "happy": ["happy", "{user} is happy"],
    "nom": ["nom", "nom nom {user} "],
    "wink": ["wink", "{user} winked"],
    "cringe": ["cringe", "Cringe fr! {user}"],
    "dance": ["dance", "{user} is dancing like a pro"],
}

reactions_double = {
    "kill": ["kill", "{user} killed {target}"],
    "slap": ["slap", "{user} slapped {target}"],
    "kick": ["kick", "{user} kicked {target}"],
    "cuddle": ["cuddle", "{user} cuddles {target}"],
    "kiss": ["kiss", "{user} kissed {target} :O"],
    "hug": ["hug", "{user} hugs {target} :}"],
    "pat": ["pat", "{user} pets {target}"],
    "bully": ["bully", "{user} bullies {target}, POG"],
    "harass": ["bully", "{user} bullies {target}"],
    "lick": ["lick", "{user} licked {target}"],
    "bite": ["bite", "{user} bit {target}"],
    "bonk": ["bonk", "{user} bonked {target}"],
    "poke": ["poke", "{user} poked {target}"],
}


async def fetch_waifu_api(endpoint: str | None = None) -> str:

    if endpoint is None:
        endpoint = "waifu" if random.randint(0, 100) > 30 else "neko"

    url = f"https://waifu.pics/api/sfw/{endpoint}"

    async with httpx.AsyncClient() as client:
        waifu_resp = await client.get(url)

    waifu_resp_json = json.loads(waifu_resp.text)
    return waifu_resp_json.get("url", None)


async def get_waifu_embed():

    embd = Embed(title="Waifu Picture")

    url = await fetch_waifu_api()
    embd.set_image(url=url)

    return embd


async def get_reaction_embed(reaction: str, user: User | Member, target: Member):

    reaction = reaction.lower()

    if reaction not in all_single_reactions and reaction not in all_double_reactions:
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

    try:
        endpoint = reactions_single[reaction][0]
        title = reactions_single[reaction][1].format(user=user.name)

    except Exception:  # noqa: BLE001
        try:
            endpoint = reactions_double[reaction][0]
            title = reactions_double[reaction][1].format(
                user=user.name, target=target.name
            )
        except Exception:  # noqa: BLE001
            pass

    url = await fetch_waifu_api(endpoint)

    embd = Embed(title=title, color=config.NORMAL_COLOR).set_image(url=url)

    return embd
