from utils.bot import Bot
from managers import mongo_manager, cache_manager
import config


def main():
    # init data items
    config.initialize_config_vars()

    # cache data
    cache_manager.init_cache()

    # load databases
    mongo_manager.init_motor()

    bot: Bot = Bot()

    bot.run(config.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
