from discord import Embed

import requests

import config

async def get_anime_details(name:str) -> dict:
    query = '''
        query ($search : String) { 
        Media (search:$search, type: ANIME) { 
            id
            title {
                romaji
                english
                native
            }
            description(asHtml: false)
            siteUrl
            genres
            episodes
            duration
            status
            coverImage {
                large
            }
            startDate{
                day
                month
                year
            }
            averageScore
            meanScore
            favourites
            format
        }
        }
    '''

    # Define our query variables and values that will be used in the query request
    variables = {
        "search" : name
    }

    url = 'https://graphql.anilist.co'

    resp = requests.post(url, json={"query" : query, "variables" : variables})

    print(resp.json())

    return resp.json()

async def get_anime_details_embed(name:str) -> Embed:

    data = await get_anime_details(name)
    data = data["data"]["Media"]

    embd:Embed = Embed(title="#{id} - {eng_name}".format(id=data["id"], eng_name=data["title"]["english"]), color=config.NORMAL_COLOR, url=data["siteUrl"])
    embd.description = data["description"][:200] + "..."
    embd.set_thumbnail(url=data["coverImage"]["large"])


    titles = list(data["title"].values())
    embd.add_field(
        name="Titles",
        value="\n".join(titles),
        inline=True
    )

    embd.add_field(
        name="Genres",
        value="\n".join(list(data["genres"])),
        inline=True
    )

    startDate = [str(x) for x in list(data["startDate"].values())]
    embd.add_field(
        name="Start Date",
        value="\n".join(startDate),
        inline=True
    )

    embd.add_field(
        name="Average Score",
        value=str(data["averageScore"]),
        inline=True
    )

    embd.add_field(
        name="Mean Score",
        value=str(data["meanScore"]),
        inline=True
    )

    embd.add_field(
        name="Favourites",
        value=str(data["favourites"]),
        inline=True
    )

    embd.add_field(
        name="Episodes",
        value=str(data["episodes"]),
        inline=True
    )

    embd.add_field(
        name="Duration",
        value=str(data["duration"]),
        inline=True
    )

    embd.add_field(
        name="Status",
        value=data["status"],
        inline=True
    )

    return embd