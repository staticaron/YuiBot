from discord import Embed
from discord.ext import pages
import requests

from views.scroller import Scroller
from queries.media_queries import recommendation_query
import config


async def get_random_anime_quote_embed() -> Embed:

    url = "https://animechan.vercel.app/api/random"

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


async def get_similar_anime(media_id: int) -> pages.Paginator:

    recommendation_resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query": recommendation_query,
            "variables": {
                "id": media_id
            }
        }
    ).json()

    recommendation_data = recommendation_resp["data"]["Page"]["recommendations"]

    pages = []

    for page_data in recommendation_data:

        recommendation = page_data["mediaRecommendation"]

        title = (page_data["media"]["title"]["english"] if page_data["media"]["title"]
                 ["english"] is not None else page_data["media"]["title"]["romaji"])

        embd = Embed(
            title="Anime similar to {}".format(title),
            color=config.NORMAL_COLOR
        )

        recommendation_title = (recommendation["title"]["english"] if recommendation["title"]
                                ["english"] is not None else recommendation["title"]["romaji"])

        embd.description = "**Name : ** [{name}]({url})\n\n**Rating : ** {rating}\n\n**Description** : {desc}".format(
            name=recommendation_title,
            url=recommendation["siteUrl"],
            rating=page_data["rating"],
            desc=recommendation["description"][:300] + "..."
        )

        embd.add_field(
            name="Genre",
            value="\n".join("{bullet}{genre}".format(
                bullet=config.BULLET_EMOTE, genre=genre) for genre in recommendation["genres"])
        )

        embd.set_thumbnail(url=recommendation["coverImage"]["medium"])

        pages.append(embd)

    if len(pages) > 0:
        return Scroller(pages)
    else:
        return None
