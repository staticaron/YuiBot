import os
import re

from discord.ext import commands
from discord import Intents, Message, Embed, Guild
from discord import __version__

from managers import cache_manager
from views.spotify_view import SpotifyView
from helpers import spotify_helper, general_helper
import config


@general_helper.with_typing_msg()
async def process_spotify_links(message: Message):
    server_details = await cache_manager.manager.get_server(message.guild.id, True)

    if server_details.get("spotify").get("enabled") is True:
        splits = message.content.strip().split()
        track_id_match = re.findall(r"(?<=track/)\w+", splits[0]) if len(splits) > 0 else None

        if len(track_id_match) > 0:
            links: spotify_helper.SpotifyTrackAlternative = await spotify_helper.get_alternatives(message=message, spotify_track_id=track_id_match[0])

            if server_details.get("spotify").get("style") == "embed":
                embd: Embed = await general_helper.get_information_embed(title="Alternate Links", description="")
                embd.description += "**Name : **" + links.track_name
                embd.description += "\n**Artists: **" + links.track_artists
                view = SpotifyView(links)

                await message.reply(embed=embd, view=view)
            elif server_details.get("spotify").get("style") == "text":
                message = await message.reply(
                    "**Name :** {}, **Artists :** {} | [Youtube Music]({})".format(
                        links.track_name,
                        links.track_artists,
                        links.youtube_music,
                    )
                )

                await message.edit(suppress=True)


class Bot(commands.Bot):
    intents: Intents = Intents.default()
    intents.message_content = True

    mentions = ["<@991739924250362047>", "<@!991739924250362047>"]

    mention_embed = None

    def prefix_callable(self, bot, msg):
        return ["yui ", "Yui ", "<@991739924250362047> ", "<@!991739924250362047> "]

    def __init__(self):
        super().__init__(command_prefix=self.prefix_callable, intents=self.intents)
        self.remove_command("help")

        # load extensions
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                self.load_extension(f"cogs.{file[:-3]}")

    async def on_ready(self):
        print("Logged in as {}".format(self.user))
        print("Discord Version : {}".format(__version__))

    async def on_message(self, message: Message):
        if message.content.strip() in self.mentions:
            embd = Embed(
                title="Ya-Ho :wave:",
                description=f"Prefix : **yui**\nLatency : **{round(self.latency * 1000, 2)} ms**\nInvite : [Click Here]({config.INVITE})",
                color=config.NORMAL_COLOR,
            ).set_thumbnail(url=self.user.avatar.url)

            return await message.channel.send(embed=embd)

        await self.process_commands(message)

        SPOTIFY_TRACK_BASE = "https://open.spotify.com/track/"

        if message.content.strip().startswith(SPOTIFY_TRACK_BASE):
            await process_spotify_links(message)

    async def on_guild_join(self, guild: Guild):
        await cache_manager.manager.register_server(guild.id, guild.name)
