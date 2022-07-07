from utils.bot import Bot
from managers import mongo_manager
import config

def main():
    # cache data items
    config.initialize_config_vars()

    # load databases
    mongo_manager.init_motor()
    
    bot:Bot = Bot()

    bot.run(config.DISCORD_TOKEN)

if __name__ == "__main__":
    main()