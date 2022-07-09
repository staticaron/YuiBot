from discord import Embed, Member
import requests

async def fetch_waifu_api(endpoint:str) -> str:
    
    url = "https://waifu.pics/api/sfw/{}".format(endpoint)
    waifu_resp = requests.get(url).json()

    try:
        return waifu_resp["url"]
    except:
        return None

async def get_random_anime_quote_embed() -> Embed:

    url="https://animechan.vercel.app/api/random"

    quote_resp = requests.get(url).json()

    embd = Embed(
        title="Anime Quote"
    )

    embd.add_field(
        name="Anime",
        value=quote_resp["anime"],
        inline=True
    )

    embd.add_field(
        name="Character",
        value=quote_resp["character"],
        inline=True
    )

    embd.add_field(
        name="Quote",
        value=quote_resp["quote"],
        inline=False
    )

    return embd

async def get_waifu_embed():

    embd = Embed(
        title="Waifu Picture"
    )

    url = await fetch_waifu_api("waifu")
    embd.set_image(url=url)

    return embd