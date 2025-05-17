import sys
import traceback

from discord import Embed
from pymongo import MongoClient, database, collection

from managers import mongo_manager
from data import base_db_entries
import config


CACHED_GENRE_EMBED = None


# converts nested dicts to mongodb compatible dicts.
def flatten_dict(normal: dict) -> dict:
    flatten_dict_output = {}

    for i in normal.items():
        if type(i[1]) is dict:
            flat_dict: dict = flatten_dict(i[1])

            for j in flat_dict.items():
                flatten_dict_output[i[0] + "." + j[0]] = j[1]
        else:
            flatten_dict_output[i[0]] = i[1]

    return flatten_dict_output


# updates nested dicts.
def nested_update(original: dict, update: dict) -> dict:
    for key, value in update.items():
        if isinstance(value, dict) and isinstance(original.get(key), dict):
            original[key] = {**original[key], **value}
        else:
            original[key] = value

    return original


class CacheManager:
    db: database.Database = None

    server_collection: collection.Collection = None

    server_cache: dict = {
        # "server_id" : <data>,
    }

    def __init__(self) -> None:
        client: MongoClient = MongoClient(config.MONGO_SRV)

        self.db: database.Database = client[config.DB]

        self.server_collection = self.db["servers"]

        count = self.cache_servers_data()

        print(f"{count} Servers Cached!")

    def cache_servers_data(self) -> int:
        """Bulk load all the data from db to cache and return the count"""

        data = self.server_collection.find({}, {"_id": 0}).to_list()
        count = 0
        for data_item in data:
            self.server_cache[data_item.get("server_id")] = data_item
            count = count + 1

        return count

    async def get_server(self, server_id: int, register_if_not_found: bool = False, server_name: str = "<none>") -> dict:
        """Fetch server from cache"""

        server_details = self.server_cache.get(server_id, None)

        if server_details is None and register_if_not_found is True:
            server_details = await self.register_server(server_id, server_name)

        return server_details

    async def register_server(self, server_id: int, server_name: str) -> None:
        """Register the guild on both db and cache"""

        existing_server = self.server_cache.get(server_id, None)

        new_entry = base_db_entries.base_servers_entry

        new_entry["server_id"] = server_id
        new_entry["server_name"] = server_name

        if existing_server is None:
            await mongo_manager.manager.add_server(new_entry)

        self.server_cache[server_id] = new_entry

        return new_entry

    async def update_server(self, server_id: int, update_details: dict) -> dict:
        """Update the server details on both db and cache"""

        existing_server: dict = self.server_cache.get(server_id, None)

        if existing_server is None:
            return

        updated_server = nested_update(existing_server, update_details)

        flatten_updated_values = flatten_dict(update_details)

        await mongo_manager.manager.update_server(server_id, flatten_updated_values)

        self.server_cache[server_id] = updated_server


def init():
    init_cache()
    init_manager()


manager: CacheManager = None


def init_manager() -> None:
    global manager

    manager = CacheManager()


def init_cache():
    try:
        cache_genre_embed()
    except Exception as e:
        print("Error while caching data")
        traceback.print_exception(type(e), e, e.__traceback__, sys.stderr)


def cache_genre_embed():
    global CACHED_GENRE_EMBED

    CACHED_GENRE_EMBED = Embed(title="Valid Genre List", color=config.NORMAL_COLOR)

    CACHED_GENRE_EMBED.description = "A combination of these genre is Valid."

    genre_pair = [
        "\n".join(config.ALL_GENRE[:7]).upper(),
        "\n".join(config.ALL_GENRE[7:13]).upper(),
        "\n".join(config.ALL_GENRE[13:]).upper(),
    ]

    for i in genre_pair:
        CACHED_GENRE_EMBED.add_field(name="Valid", value=i, inline=True)
