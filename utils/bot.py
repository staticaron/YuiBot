from discord.ext import commands
from discord import Intents, Message, Embed
from discord import __version__
import os

import config


class Bot(commands.Bot):
    intents: Intents = Intents.default()
    intents.message_content = True

    mentions = ["<@991739924250362047>", "<@!991739924250362047>"]

    mention_embed = None

    def prefix_callable(self, bot, msg):
        return ["yui ", "Yui ", "<@991739924250362047> ", "<@!991739924250362047> "]

    def __init__(self):
        super().__init__(command_prefix=self.prefix_callable, intents=self.intents)

        # load extensions
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                self.load_extension(f"cogs.{file[:-3]}")

    async def on_ready(self):
        print("Logged in as {}".format(self.user))
        print("Discord Version : {}".format(__version__))

    async def on_message(self, message: Message):

        if message.content.strip() in self.mentions:

            embd = Embed(title="Ya-Ho :wave:",
                         description=f"Prefix : **yui**\nLatency : **{round(self.latency * 1000, 2)} ms**\nInvite : [Click Here]({config.INVITE})", color=config.NORMAL_COLOR).set_thumbnail(url=self.user.avatar.url)

            await message.channel.send(embed=embd)
