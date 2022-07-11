from discord.ext import commands
from discord import Intents
from discord import __version__
import os

class Bot(commands.Bot):

    bot:commands.Bot = None
    intents:Intents = Intents.default()
    intents.message_content = True

    def prefix_callable(self, bot, msg):
        return ["yui ", "Yui "]

    def __init__(self):
        super().__init__(command_prefix=self.prefix_callable, intents=self.intents)

        #load extensions
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                self.load_extension(f"cogs.{file[:-3]}")

    async def on_ready(self):
        print("Logged in as {}".format(self.user))
        print("Discord Version : {}".format(__version__))