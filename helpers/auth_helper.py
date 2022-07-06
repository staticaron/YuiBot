import requests

from config import ANILIST_BASE
from helpers import general_helper

async def get_user_from_username(username:str):

    query = """
        query($username:String){
            User(search:$username){
                id
                name
                siteUrl
                avatar{
                    medium
                }
            }
        }
    """

    variables = {
        "username" : username
    }

    resp = requests.post(ANILIST_BASE, json={
        "query" : query,
        "variables" : variables
    })

    data = resp.json()

    if data["data"]["User"] is None:
        return None

    profile_embd = await general_helper.get_information_embed(
        title="Is this your Profile?",
        url=data["data"]["User"]["siteUrl"],
        description="**Name :** {name} \n\nIf yes send **Yes** else send **No**".format(name=data["data"]["User"]["name"]),
        thumbnail_link=data["data"]["User"]["avatar"]["medium"]
    )

    return profile_embd

