import tracemoepy
from discord import Embed
from tracemoepy.errors import ServerError, TooManyRequests

from config import ERROR_COLOR, NORMAL_COLOR
from helpers import general_helper
from managers.logging_manager import get_logger
from views.scroller import Scroller

logger = get_logger()

"""Returns a list of matched anime"""


async def get_all_detected_anime_scroller(url: str) -> Scroller | Embed:

    async with tracemoepy.AsyncTrace() as tracemoe:
        try:
            quota = await tracemoe.get_me()
            logger.info(f"Tracemoe Call Initialized! Remaining Searches : {quota['quota']}")
            logger.info(f"Tracemoe Url Requested : {url}")

            image_extensions = [".png", ".gif", ".jpg", ".webp", ".jpeg"]
            image_url = any(x in url for x in image_extensions)

            if not image_url:
                return await general_helper.get_information_embed("Failed!", ERROR_COLOR, None, "Please provide a valid image URL")

            results = await tracemoe.search(url, is_url=True)
        except TooManyRequests:
            return await general_helper.get_information_embed(title="Too Many Requests", color=ERROR_COLOR)
        except ServerError:
            return await general_helper.get_information_embed(title="Image Error", color=ERROR_COLOR)
        else:
            embds = []

            sfw_results = [x for x in results.result if x.anilist.isAdult is False]

            for result in sfw_results:
                name = result.anilist.title.english or result.anilist.title.native

                image = result.image
                similarity = str(round(result.similarity * 100, 3)) + "%"
                url = f"https://anilist.co/anime/{result.anilist.id}/"
                video = result.video

                embd = Embed(title="Detected", color=NORMAL_COLOR, description="")
                embd.description = f"**Name** : [{name}]({url})\n**Similarity** : {similarity}\n**Reference : [click here]({video})**"

                embd.set_image(url=image)

                embds.append(embd)

            return Scroller(embed_pages=embds, show_all_btns=True)
