import sys

from utils.bot import Bot
from utils import logger
from managers import mongo_manager, cache_manager

import config


def main(test=False):
    print("""
    .%%..%%..%%..%%..%%%%%%..%%%%%....%%%%...%%%%%%.
    ..%%%%...%%..%%....%%....%%..%%..%%..%%....%%...
    ...%%....%%..%%....%%....%%%%%...%%..%%....%%...
    ...%%....%%..%%....%%....%%..%%..%%..%%....%%...
    ...%%.....%%%%...%%%%%%..%%%%%....%%%%.....%%...
    ................................................
    """)

    logger.setup_logger(test)

    config.initialize_config_vars()
    cache_manager.init()
    mongo_manager.init_motor()

    logger.logger.warning("Components Loaded!")

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
