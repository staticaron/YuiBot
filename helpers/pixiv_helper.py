import pixivapi

async def search_embed(value:str):

    client = pixivapi.Client(language="English")

    client.login("redesign101", "myPixiv@19")

    illustrations = await client.search_illustrations(value)

    print(illustrations)

