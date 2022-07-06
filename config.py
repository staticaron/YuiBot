from discord import Color
from os import environ

DISCORD_TOKEN = None
ANILIST_ID = None
ANILIST_TOKEN = None
INVITE = None

# URL Bases
ANILIST_BASE = "https://graphql.anilist.co"
ANILIST_LOGIN = "https://anilist.co/api/v2/oauth/authorize?client_id={client_id}&response_type=code"

# Colors
NORMAL_COLOR = Color.dark_theme()
ERROR_COLOR = Color.red()

# Emojis
YUI_SHY_EMOTE="<a:yui_shy:991749482763014184>"
ADULT_CONTENT_EMOTE="<:18_up:991930483309023352>"
BULLET_EMOTE="<:bullet:992560047978729512>"
DOT_EMOTE="<:dots:993535564835979357>"
LOADING_EMOTE="<a:LOADING:994182649100894318>"

def initialize_config_vars() -> str:
    global DISCORD_TOKEN, ANILIST_ID, ANILIST_TOKEN, INVITE

    try:
        DISCORD_TOKEN = environ["TOKEN"]
        ANILIST_TOKEN = environ["ANILIST_TOKEN"]
        ANILIST_ID = environ["ANILIST_ID"]
        INVITE = environ["INVITE"]
    except Exception as e:
        return f"Error occurred while trying to cache Config Vars! \n{e}"
    else:
        return "Config Vars were cached successfully!"