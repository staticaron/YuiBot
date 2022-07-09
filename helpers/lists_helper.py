import requests

import config

async def add_ptw(anime:str):

    anime_query = """
        query($search:String){
            Page(page:0, perPage:5){
                pageInfo{
                    total
                }
                media(search:$search, sort:SEARCH_MATCH, type:ANIME){
                    id 
                    title{
                        english
                        romaji
                    }
                    genres
                    coverImage{
                        medium
                    }
                    episodes
                    status
                }
            }
        }
    """

    variables = {
        "search" : anime
    }

    anime_resp = requests.post(
        url=config.ANILIST_BASE,
        json={
            "query" : anime_query,
            "variables" : variables
        }
    )

    print(anime_resp.json())