from discord import Embed, Member
import requests

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
