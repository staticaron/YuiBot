from discord import Embed
import traceback
import sys

from config import ALL_GENRE, NORMAL_COLOR

CACHED_GENRE_EMBED = None


def init_cache():
    try:
        cache_genre_embed()
    except Exception as e:
        print("Error while caching data")
        traceback.print_exception(type(e), e, e.__traceback__, sys.stderr)
    else:
        print("Data cached successfully")


def cache_genre_embed():
    global CACHED_GENRE_EMBED

    CACHED_GENRE_EMBED = Embed(title="Valid Genre List", color=NORMAL_COLOR)
    CACHED_GENRE_EMBED.description = "A combination of these genre is Valid."

    genre_pair = ["\n".join(ALL_GENRE[:7]).upper(),
                  "\n".join(ALL_GENRE[7:13]).upper(),
                  "\n".join(ALL_GENRE[13:]).upper()]

    for i in genre_pair:
        CACHED_GENRE_EMBED.add_field(
            name="Valid",
            value=i,
            inline=True
        )
