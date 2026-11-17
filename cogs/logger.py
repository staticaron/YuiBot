from discord import Guild, Thread
from discord.abc import GuildChannel, PrivateChannel
from discord.ext import commands

from config import (
    ERROR_COLOR,
    SERVER_LOG_CHANNEL,
    SUPPORT_SERVER_LINK,
    VOTE_LINK,
    YUI_SHY_EMOTE,
)
from helpers import general_helper
from managers.logging_manager import get_logger

logger = get_logger()


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.welcome_embd = None
        self.server_log_channel: GuildChannel | Thread | PrivateChannel | None = None
        self.general_chat_channel_names = [
            "general",
            "chat",
            "lounge",
            "main",
            "talk",
            "chatting",
            "talking",
        ]

    @commands.Cog.listener("on_ready")
    async def load(self):
        self.server_log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL)

        self.welcome_embd = await general_helper.get_information_embed(
            title="Arigatou!",
            description=f"Thanks for inviting me to this server. {YUI_SHY_EMOTE}\n\nYourAnimeBot is your most powerful anilist companion bot which allows anyone to fetch/modify/display their anilist data without leaving discord. It is packed with easy to use and intuitive commands. \n\n**Prefix** : yui and {self.bot.user.mention}\n**Help Command** : yui help\n\n*Try `yui info` to get started. Make sure you first use `yui login` to log in with your anilist account.* \n\n**Support Server** : [Click Here]({SUPPORT_SERVER_LINK})\n**Vote** : [Click Here]({VOTE_LINK})",
            thumbnail_link=self.bot.user.avatar.url if self.bot.user is not None and self.bot.user.avatar is not None else "",
        )

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild: Guild):

        if self.server_log_channel is None:
            return

        await self.server_log_channel.send(
            embed=await general_helper.get_information_embed(
                title="Server Added!",
                description=f"Name : **{guild.name}**\nMember Count : **{guild.member_count}**\nTotal Server Count : **{len(self.bot.guilds)}**",
                thumbnail_link=self.bot.user.avatar.url if self.bot.user is not None and self.bot.user.avatar is not None else "",
            )
        )

        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                if channel == guild.system_channel or any(x in channel.name for x in self.general_chat_channel_names):
                    await channel.send(embed=self.welcome_embd)
                    break
            else:
                logger.error(f"Can't send messages in # {channel.name}")
                continue

    @commands.Cog.listener("on_guild_remove")
    async def on_guild_remove(self, guild: Guild):
        await self.server_log_channel.send(
            embed=await general_helper.get_information_embed(
                title="Server Removed!",
                description=f"Name : **{guild.name}**\nMember Count : **{guild.member_count}**\nTotal Server Count : **{len(self.bot.guilds)}**",
                thumbnail_link=self.bot.user.avatar.url,
                color=ERROR_COLOR,
            )
        )


def setup(bot):
    bot.add_cog(Logger(bot))
