from discord import Embed
import requests

async def fetch_waifu_api(endpoint:str) -> str:
    
    url = "https://waifu.pics/api/sfw/{}".format(endpoint)
    waifu_resp = requests.get(url).json()

    try:
        return waifu_resp["url"]
    except:
        return None

async def get_waifu_embed():

    embd = Embed(
        title="Waifu Picture"
    )

    url = await fetch_waifu_api("waifu")
    embd.set_image(url=url)

    return embd