from discord import Embed
import tracemoepy
from tracemoepy.errors import *

from views.scroller import Scroller
from helpers import general_helper
from config import NORMAL_COLOR, ERROR_COLOR


"""Returns a list of matched anime"""


async def get_all_detected_anime_scroller(url: str):

    async with tracemoepy.AsyncTrace() as tracemoe:
        try:
            results = await tracemoe.search(url, is_url=True)
        except TooManyRequests as t:
            return await general_helper.get_information_embed(title="Too Many Requests", color=ERROR_COLOR)
        except ServerError as s:
            return await general_helper.get_information_embed(title="Image Error", color=ERROR_COLOR)
        else:
            embds = []

            sfw_results = [x for x in results.result if x.anilist.isAdult is False]

            for result in sfw_results:

                name = result.anilist.title.english or result.anilist.title.native

                image = result.image
                similarity = str(round(result.similarity * 100, 3)) + "%"
                url = "https://anilist.co/anime/{}/".format(result.anilist.id)
                video = result.video

                embd = Embed(title="Detected", color=NORMAL_COLOR, description="")
                embd.description += "**Name** : [{}]({})\n**Similarity** : {}\n**Reference : [click here]({})**".format(
                    name, url, similarity, video)

                embd.set_image(url=image)

                embds.append(embd)

            return Scroller(embed_pages=embds, show_all_btns=True)