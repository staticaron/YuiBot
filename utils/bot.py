import os
import re

from discord import Embed, Guild, Intents, Message, __version__
from discord.ext import commands

import config
from helpers import general_helper, spotify_helper
from managers import cache_manager
from managers.logging_manager import get_logger
from views.spotify_view import SpotifyView

logger = get_logger()


@general_helper.with_typing_msg()
async def process_spotify_links(message: Message):

    if message.guild is None:
        return

    server_details: dict | None = await cache_manager.manager.get_server(message.guild.id, True)

    if server_details is None:
        return

    if server_details.get("spotify", {}).get("enabled", False) is True:
        splits = message.content.strip().split()

        if len(splits) <= 0:
            return

        track_id_match: list = re.findall(r"(?<=track/)\w+", splits[1])
        if len(track_id_match) > 0:
            links: spotify_helper.SpotifyTrackAlternative | None = await spotify_helper.get_alternatives(message=message, spotify_track_id=track_id_match[0])
            if links is None:
                return

            if server_details.get("spotify", {}).get("style", "text") == "embed":
                embd: Embed = await general_helper.get_information_embed(title="Alternate Links", description="")
                embd.description = "**Name : **" + links.track_name
                embd.description += "\n**Artists: **" + links.track_artists
                view = SpotifyView(links)

                await message.reply(embed=embd, view=view)
            elif server_details.get("spotify", {}).get("style", "text") == "text":
                message = await message.reply(f"**Name :** {links.track_name}, **Artists :** {links.track_artists} | [Youtube Music]({links.youtube_music})")

                await message.edit(suppress=True)


class Bot(commands.Bot):
    def prefix_callable(self, bot, msg):
        return ["yui ", "Yui ", "<@991739924250362047> ", "<@!991739924250362047> "]

    def __init__(self):
        super().__init__(command_prefix=self.prefix_callable, intents=Intents.default())
        self.remove_command("help")
        self.mentions = ["<@991739924250362047>", "<@!991739924250362047>"]
        self.mention_embed = None

        # load extensions
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                self.load_extension(f"cogs.{file[:-3]}")

    async def on_ready(self):
        logger.info(f"Logged in as {self.user}")
        logger.info(f"Discord Version : {__version__}")

    async def on_message(self, message: Message):
        if message.content.strip() in self.mentions:
            embd = Embed(
                title="Ya-Ho :wave:",
                description=f"Prefix : **yui**\nLatency : **{round(self.latency * 1000, 2)} ms**\nInvite : [Click Here]({config.INVITE})",
                color=config.NORMAL_COLOR,
            ).set_thumbnail(url=self.user.avatar.url if self.user is not None and self.user.avatar is not None else "")

            await message.channel.send(embed=embd)
            return

        await self.process_commands(message)

        SPOTIFY_TRACK_BASE = "https://open.spotify.com/track/"

        if SPOTIFY_TRACK_BASE in message.content.strip():
            await process_spotify_links(message)

    async def on_guild_join(self, guild: Guild):
        await cache_manager.manager.register_server(guild.id, guild.name)
