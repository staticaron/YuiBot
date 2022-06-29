from discord.ext import commands

from utils.bot import Bot
import config

def main():
    # cache data items
    config.initialize_config_vars()

    # load databases
    
    bot:Bot = Bot()

    bot.run(config.TOKEN)

if __name__ == "__main__":
    main()