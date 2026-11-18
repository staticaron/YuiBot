import sys

import config
from managers import cache_manager, logging_manager, mongo_manager
from utils.bot import Bot

logging_manager.setup_logging()


def main(test=False):
    print("""
    .%%..%%..%%..%%..%%%%%%..%%%%%....%%%%...%%%%%%.
    ..%%%%...%%..%%....%%....%%..%%..%%..%%....%%...
    ...%%....%%..%%....%%....%%%%%...%%..%%....%%...
    ...%%....%%..%%....%%....%%..%%..%%..%%....%%...
    ...%%.....%%%%...%%%%%%..%%%%%....%%%%.....%%...
    ................................................
    """)

    config.initialize_config_vars()

    cache_manager.init()
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
