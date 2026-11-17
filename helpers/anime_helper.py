import json

import httpx
from discord import Embed
from discord.ext import pages

import config
from queries.media_queries import recommendation_query
from views.scroller import Scroller


async def get_random_anime_quote_embed() -> Embed:

    url = "https://animechan.vercel.app/api/random"

    async with httpx.AsyncClient() as client:
        quote_resp_raw = await client.get(url)

    quote_resp = json.loads(quote_resp_raw.text)

    embd = Embed(title="Anime Quote")

    embd.add_field(name="Anime", value=quote_resp["anime"], inline=True)
    embd.add_field(name="Character", value=quote_resp["character"], inline=True)
    embd.add_field(name="Quote", value=quote_resp["quote"], inline=False)

    return embd


async def get_similar_anime(media_id: int) -> pages.Paginator | None:

    async with httpx.AsyncClient() as client:
        recommendation_resp_raw = await client.post(
            url=config.ANILIST_BASE,
            json={"query": recommendation_query, "variables": {"id": media_id}},
        )

    recommendation_resp = json.loads(recommendation_resp_raw.text)
    recommendation_data = recommendation_resp["data"]["Page"]["recommendations"]

    pages = []

    for page_data in recommendation_data:
        recommendation = page_data["mediaRecommendation"]

        title = (
            page_data["media"]["title"]["english"]
            if page_data["media"]["title"]["english"] is not None
            else page_data["media"]["title"]["romaji"]
        )

        embd = Embed(title=f"Anime similar to {title}", color=config.NORMAL_COLOR)

        recommendation_title = (
            recommendation["title"]["english"]
            if recommendation["title"]["english"] is not None
            else recommendation["title"]["romaji"]
        )

        embd.description = "**Name : ** [{name}]({url})\n\n**Rating : ** {rating}\n\n**Description** : {desc}".format(
            name=recommendation_title,
            url=recommendation["siteUrl"],
            rating=page_data["rating"],
            desc=recommendation["description"][:300] + "...",
        )

        embd.add_field(
            name="Genre",
            value="\n".join(
                f"{config.BULLET_EMOTE}{genre}" for genre in recommendation["genres"]
            ),
        )

        embd.set_thumbnail(url=recommendation["coverImage"]["medium"])

        pages.append(embd)

    if len(pages) > 0:
        return Scroller(pages)
    else:
        return None
