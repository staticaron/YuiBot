from discord import Member
from discord.ext import commands

from helpers import user_helper

class UserModule(commands.Cog):

    @commands.command(name="follow", aliases=["addfollow"], description="Add the mentioned user to the following list.")
    async def follow_user(self, ctx:commands.Context, target:Member):

        reply = await user_helper.follow_user(ctx.author, target)

        await ctx.reply(embed=reply)

    @commands.command(name="unfollow", aliases=["removefollow"], description="Add the mentioned user to the following list.")
    async def unfollow_user(self, ctx:commands.Context, target:Member):

        reply = await user_helper.unfollow_user(ctx.author, target)

        await ctx.reply(embed=reply)

def setup(bot:commands.Bot):
    bot.add_cog(UserModule())