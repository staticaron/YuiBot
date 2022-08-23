from discord.ext import commands
from discord import Guild, TextChannel

from helpers import general_helper
from config import SERVER_LOG_CHANNEL, ERROR_COLOR


class Logger(commands.Cog):

    bot: commands.Bot = None
    server_log_channel: TextChannel = None

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def load(self):
        self.server_log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL)

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild: Guild):
        await self.server_log_channel.send(embed=await general_helper.get_information_embed(title="Server Added!", description="Name : **{name}**\nMember Count : **{count}**\nTotal Server Count : **{total}**".format(name=guild.name, count=guild.member_count, total=len(self.bot.guilds)), thumbnail_link=self.bot.user.avatar.url))

    @commands.Cog.listener("on_guild_remove")
    async def on_guild_remove(self, guild: Guild):
        await self.server_log_channel.send(embed=await general_helper.get_information_embed(title="Server Removed!", description="Name : **{name}**\nMember Count : **{count}**\nTotal Server Count : **{total}**".format(name=guild.name, count=guild.member_count, total=len(self.bot.guilds)), thumbnail_link=self.bot.user.avatar.url, color=ERROR_COLOR))


def setup(bot):
    bot.add_cog(Logger(bot))
