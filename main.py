import sys

from utils.bot import Bot
from managers import mongo_manager, cache_manager
import config


def main(test=False):
    # init data items
    config.initialize_config_vars()

    # cache data
    cache_manager.init_cache()

    # load databases
    mongo_manager.init_motor()

    bot: Bot = Bot()

    if test:
        bot.run(config.DISCORD_TEST_TOKEN)
    else:
        bot.run(config.DISCORD_TOKEN)


if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1].lower() == "true":
        main(True)
    else:
        main(False)
       
