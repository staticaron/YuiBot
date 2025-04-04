from discord import Color
from os import environ
import json
import traceback
import sys
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = None
DISCORD_TEST_TOKEN = None
ANILIST_ID = None
ANILIST_TOKEN = None
MONGO_SRV = None
DB = "youranimedb"
INVITE = None
SUPPORT_SERVER_LINK = "https://discord.gg/AbfZPyx5MH"
VOTE_LINK = "https://top.gg/bot/991739924250362047"

# Loggers
SERVER_LOG_CHANNEL = 1011530425023344722

# URL Bases
ANILIST_BASE = "https://graphql.anilist.co"
ANILIST_LOGIN = "https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&response_type=token"

CHIAKI_BASE = "https://chiaki.vercel.app/get?group_id={}"

# Colors
NORMAL_COLOR = Color.dark_theme()
INFO_COLOR = Color.gold()
ERROR_COLOR = Color.red()

# Emojis
YUI_SHY_EMOTE = "<a:yui_shy:991749482763014184>"
ADULT_CONTENT_EMOTE = "<:18_up:991930483309023352>"
BULLET_EMOTE = "<:bullet:992560047978729512>"
DOT_EMOTE = "<:dots:993535564835979357>"
LOADING_EMOTE = "<a:LOADING:994182649100894318>"
NEXT_EMOTE = "<:next:995484808207683604>"
PREV_EMOTE = "<:prev:995484847139209238>"
FIRST_EMOTE = "<:first:996104181515571201>"
LAST_EMOTE = "<:last:996104225459277854>"

FILLER_DATA = None

ALL_GENRE = ["action", "adventure", "comedy", "drama", "ecchi", "fantasy", "hentai", "horror", "mecha",
             "music", "mystery", "psychological", "romance", "sci-fi", "sol", "sports", "supernatural", "thriller"]

ALL_GENRE_ALTS = {
    "action": "Action",
    "adventure": "Adventure",
    "comedy": "Comedy",
    "drama": "Drama",
    "ecchi": "Ecchi",
    "fantasy": "Fantasy",
    "hentai": "Hentai",
    "horror": "Horror",
    "mecha": "Mecha",
    "music": "Music",
    "mystery": "Mystery",
    "psychological": "Psychological",
    "romance": "Romance",
    "sci-fi": "Sci-Fi",
    "sol": "Slice of Life",
    "sports": "Sports",
    "supernatural": "Supernatural",
    "thriller": "Thriller"
}

SECRET_KEY = ""


def initialize_config_vars() -> str:
    global DISCORD_TOKEN, DISCORD_TEST_TOKEN, ANILIST_ID, ANILIST_TOKEN, INVITE, MONGO_SRV, FILLER_DATA, SECRET_KEY

    load_dotenv()

    try:
        DISCORD_TOKEN = environ["TOKEN"]
        DISCORD_TEST_TOKEN = environ["TEST_TOKEN"]
        ANILIST_TOKEN = environ["ANILIST_TOKEN"]
        ANILIST_ID = environ["ANILIST_ID"]
        MONGO_SRV = environ["MONGO_SRV"]
        INVITE = environ["INVITE"]
        SECRET_KEY = environ["SECRET_KEY"]

        with open("data/filler_data.json", "r", encoding="utf8") as filler_data:
            FILLER_DATA = json.load(filler_data)

    except Exception as e:
        print(f"Error occurred while trying to cache Config Vars! \n{e}")
        traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
    else:
        print("Config Vars were cached successfully!")
