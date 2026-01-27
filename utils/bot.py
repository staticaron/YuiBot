import os
import re

from discord.ext import commands
from discord import Intents, Message, Embed, Guild
from discord import __version__

from managers import cache_manager
from views.spotify_view import SpotifyView
from helpers import spotify_helper, general_helper
from utils import logger
import config


@general_helper.with_typing_msg()
async def process_spotify_links(message: Message):
    """
    Process Spotify Links and return Youtube Music links for the same song
    """

    # ignore DMs
    if message.guild is None:
        return

    server_details = await cache_manager.manager.get_server(message.guild.id, True)

    if server_details is None:
        return

    if server_details.get("spotify", {}).get("enabled") is True:
        splits = message.content.strip().split()
        track_id_match = (
            re.findall(r"(?<=track/)\w+", splits[1]) if len(splits) > 0 else None
        )

        if track_id_match is None:
            return

        if len(track_id_match) > 0:
            links: spotify_helper.SpotifyTrackAlternative = (
                await spotify_helper.get_alternatives(
                    message=message, spotify_track_id=track_id_match[0]
                )
            )

            if server_details.get("spotify", {}).get("style") == "embed":
                embd: Embed = await general_helper.get_information_embed(
                    title="Alternate Links", description=""
                )
                embd.description = "**Name : **" + links.track_name
                embd.description += "\n**Artists: **" + links.track_artists

                view = SpotifyView(links)

                await message.reply(embed=embd, view=view)

            elif server_details.get("spotify", {}).get("style") == "text":
                message = await message.reply(
                    "**Name :** {}, **Artists :** {} | [Youtube Music]({})".format(
                        links.track_name,
                        links.track_artists,
                        links.youtube_music,
                    )
                )

                await message.edit(suppress=True)


class Bot(commands.Bot):
    custom_intents: Intents = Intents.default()

    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned, intents=self.custom_intents
        )
        self.remove_command("help")

        # load extensions
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                self.load_extension(f"cogs.{file[:-3]}")

        self.mention_embed = Embed(
            title="Ya-Ho :wave:",
            description=f"Prefix : **yui**\nLatency : **{round(self.latency * 1000, 2)} ms**\nInvite : [Click Here]({config.INVITE})",
            color=config.NORMAL_COLOR,
        )
        self.mention_embed.set_thumbnail(
            url=self.user.avatar.url
            if self.user is not None and self.user.avatar is not None
            else ""
        )

    async def on_ready(self):
        logger.logger.info("Logged in as {}".format(self.user))
        logger.logger.info("Discord Version : {}".format(__version__))

    async def on_message(self, message: Message) -> None:
        """
        Override the base on_message to extend functionality
        """

        if self.user is None:
            return

        if message.content == self.user.mention:
            await message.channel.send(embed=self.mention_embed)
            return

        await self.process_commands(message)

        SPOTIFY_TRACK_BASE = f"{self.user.mention} https://open.spotify.com/track/"

        if message.content.strip().startswith(SPOTIFY_TRACK_BASE):
            await process_spotify_links(message)

    async def on_guild_join(self, guild: Guild):
        await cache_manager.manager.register_server(guild.id, guild.name)
