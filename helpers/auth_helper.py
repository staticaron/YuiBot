import requests

from config import ANILIST_BASE
from helpers import general_helper

async def get_user_from_anilistID(anilistID:str):

    query = """
        query($anilistID:Int){
            User(id:$anilistID){
                name
                siteUrl
                avatar{
                    medium
                }
            }
        }
    """

    variables = {
        "anilistID" : anilistID
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

