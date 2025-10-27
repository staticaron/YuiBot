import pixivapi
import logging


async def searchrembed(value: str):
    client = pixivapi.Client(language="English")

    client.login("redesign101", "myPixiv@19")

    illustrations = await client.search_illustrations(value)

    logging.info(illustrations)
