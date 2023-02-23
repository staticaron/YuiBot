from discord.ext import commands
from discord import Guild, TextChannel, Permissions

from helpers import general_helper
from config import SERVER_LOG_CHANNEL, ERROR_COLOR, YUI_SHY_EMOTE, SUPPORT_SERVER_LINK, VOTE_LINK


class Logger(commands.Cog):

    bot: commands.Bot = None
    server_log_channel: TextChannel = None

    general_chat_channel_names = ["general", "chat", "lounge", "main", "talk", "chatting", "talking"]

    welcome_embd = None

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def load(self):
        self.server_log_channel = self.bot.get_channel(SERVER_LOG_CHANNEL)

        self.welcome_embd = await general_helper.get_information_embed(title="Arigatou!", description=f"Thanks for inviting me to this server. {YUI_SHY_EMOTE}\n\nYourAnimeBot is your most powerful anilist companion bot which allows anyone to fetch/modify/display their anilist data without leaving discord. It is packed with easy to use and intuitive commands. \n\n**Prefix** : yui and {self.bot.user.mention}\n**Help Command** : yui help\n\n*Try `yui info` to get started. Make sure you first use `yui login` to log in with your anilist account.* \n\n**Support Server** : [Click Here]({SUPPORT_SERVER_LINK})\n**Vote** : [Click Here]({VOTE_LINK})", thumbnail_link=self.bot.user.avatar.url)

    @commands.Cog.listener("on_guild_join")
    async def on_guild_join(self, guild: Guild):
        await self.server_log_channel.send(embed=await general_helper.get_information_embed(title="Server Added!", description="Name : **{name}**\nMember Count : **{count}**\nTotal Server Count : **{total}**".format(name=guild.name, count=guild.member_count, total=len(self.bot.guilds)), thumbnail_link=self.bot.user.avatar.url))

        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                if channel == guild.system_channel or any(x in channel.name for x in self.general_chat_channel_names):
                    await channel.send(embed=self.welcome_embd)
                    break
            else:
                print(f"Can't send messages in # {channel.name}")
                continue

    @commands.Cog.listener("on_guild_remove")
    async def on_guild_remove(self, guild: Guild):
        await self.server_log_channel.send(embed=await general_helper.get_information_embed(title="Server Removed!", description="Name : **{name}**\nMember Count : **{count}**\nTotal Server Count : **{total}**".format(name=guild.name, count=guild.member_count, total=len(self.bot.guilds)), thumbnail_link=self.bot.user.avatar.url, color=ERROR_COLOR))


def setup(bot):
    bot.add_cog(Logger(bot))
