from discord import Embed
import requests
import urllib.parse
import re

from helpers import general_helper
from config import NORMAL_COLOR, ERROR_COLOR

async def get_embed(url:str) -> Embed:

    resp = requests.get("https://api.trace.moe/search?url={}".format(urllib.parse.quote_plus(url))).json()

    try:
        top_result = resp["result"][0]
    except Exception as e:

        if resp["error"].startswith("Failed to fetch image"):
            return await general_helper.get_information_embed("Unable to Fetch Image from the url.", description="The url doesn't leads to a valid image. Url ending with `.jpg`, `.png`, `.gif` are supported.", color=ERROR_COLOR)

        return await general_helper.get_information_embed("Unable to detect.", color=ERROR_COLOR, description="The following error occurred : ```{}```".format(resp["error"]))

    name = top_result["filename"]
    name = name.replace("-", "")

    if getLeadingGateStuff(name) is not None:
        name = name.replace(getLeadingGateStuff(name), "")
    
    if getTrailingParenthesisStuff(name) is not None:
        name = name.replace(getTrailingParenthesisStuff(name), "")

    name = name.removesuffix(".mp4").strip()
    name = name.removesuffix("RAW").strip()

    image = top_result["image"]
    similarity = str(int(top_result["similarity"] * 100)) + "%"
    url = "https://anilist.co/anime/{}/".format(top_result["anilist"])
    video = top_result["video"]

    embd = Embed(title="Detected", color=NORMAL_COLOR, description="")
    embd.description += "**Name** : [{}]({})\n**Similarity** : {}\n**Reference : [click here]({})**".format(name, url, similarity, video)

    embd.set_image(url=image)

    return embd

def getLeadingGateStuff(input):
    regex = r"\[(.*?)\]"
    matches = re.findall(regex, input)

    if len(matches) > 0:
        return "[" + matches[-1] + "]"
    else:
        return None

def getTrailingParenthesisStuff(input):
    regex = r"\((.*?)\)"
    matches = re.findall(regex, input)

    if len(matches) > 0:
        return "(" + matches[-1] + ")"
    else:
        return None