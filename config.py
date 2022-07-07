from discord import Color
from os import environ

DISCORD_TOKEN = None
ANILIST_ID = None
ANILIST_TOKEN = None
MONGO_SRV = None
DB = "youranimedb"
INVITE = None

# URL Bases
ANILIST_BASE = "https://graphql.anilist.co"
ANILIST_LOGIN = "https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&response_type=token"

# Colors
NORMAL_COLOR = Color.dark_theme()
INFO_COLOR = Color.gold()
ERROR_COLOR = Color.red()

# Emojis
YUI_SHY_EMOTE="<a:yui_shy:991749482763014184>"
ADULT_CONTENT_EMOTE="<:18_up:991930483309023352>"
BULLET_EMOTE="<:bullet:992560047978729512>"
DOT_EMOTE="<:dots:993535564835979357>"
LOADING_EMOTE="<a:LOADING:994182649100894318>"

def initialize_config_vars() -> str:
    global DISCORD_TOKEN, ANILIST_ID, ANILIST_TOKEN, INVITE, MONGO_SRV

    try:
        DISCORD_TOKEN = environ["TOKEN"]
        ANILIST_TOKEN = environ["ANILIST_TOKEN"]
        ANILIST_ID = environ["ANILIST_ID"]
        MONGO_SRV = environ["MONGO_SRV"]
        INVITE = environ["INVITE"]
    except Exception as e:
        return f"Error occurred while trying to cache Config Vars! \n{e}"
    else:
        return "Config Vars were cached successfully!"