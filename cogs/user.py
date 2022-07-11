from discord import Member
from discord.ext import commands

from helpers import user_helper, general_helper

class UserModule(commands.Cog):

    @commands.command(name="user", aliases=["info"], description="Returns the details of mentioned AniList user")
    @commands.check(general_helper.validate_user)
    async def user_info(self, ctx:commands.Context, user:Member=None):
        user = (ctx.author if user is None else user)

        reply = await user_helper.get_user_embed(str(user.id))

        await ctx.send(embed=reply)

    @commands.command(name="follow", aliases=["addfollow"], description="Add the mentioned user to the following list.")
    @commands.check(general_helper.validate_user)
    async def follow_user(self, ctx:commands.Context, target:Member):

        reply = await user_helper.follow_user(ctx.author, target)

        await ctx.reply(embed=reply)

    @commands.command(name="unfollow", aliases=["removefollow"], description="Add the mentioned user to the following list.")
    @commands.check(general_helper.validate_user)
    async def unfollow_user(self, ctx:commands.Context, target:Member):

        reply = await user_helper.unfollow_user(ctx.author, target)

        await ctx.reply(embed=reply)

def setup(bot:commands.Bot):
    bot.add_cog(UserModule())