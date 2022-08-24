from discord import Member
from discord.ext import commands

from helpers import user_helper, general_helper


class UserModule(commands.Cog):

    @commands.command(name="user", aliases=["info"], description="Returns the details of mentioned AniList user")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    async def user_info(self, ctx: commands.Context, target: Member = None):

        await ctx.trigger_typing()

        target = (ctx.author if target is None else target)

        reply = await user_helper.get_user_embed(str(target.id))

        await ctx.send(embed=reply)

    @commands.command(name="follow", aliases=["addfollow"], description="Add the mentioned user to the following list.")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    async def follow_user(self, ctx: commands.Context, target: Member):

        await ctx.trigger_typing()

        reply = await user_helper.follow_user(ctx.author, target)

        await ctx.reply(embed=reply)

    @commands.command(name="unfollow", aliases=["removefollow"], description="Add the mentioned user to the following list.")
    @commands.check(general_helper.validate_user)
    async def unfollow_user(self, ctx: commands.Context, target: Member):

        await ctx.trigger_typing()

        reply = await user_helper.unfollow_user(ctx.author, target)

        await ctx.reply(embed=reply)

    @commands.command(name="animestats", aliases=["as", "statistics"], description="Returns the anime stats of a user")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    async def anime_stats(self, ctx: commands.Context, target: Member = None):

        await ctx.trigger_typing()

        target = (ctx.author if target is None else target)

        reply = await user_helper.get_user_media_stats(target, "ANIME")

        await ctx.send(embed=reply)

    @commands.command(name="mangastats", aliases=["ms"], description="Returns the manga stats of a user")
    @commands.check(general_helper.validate_user)
    @general_helper.short_cooldown()
    async def manga_stats(self, ctx: commands.Context, target: Member = None):

        await ctx.trigger_typing()

        target = (ctx.author if target is None else target)

        reply = await user_helper.get_user_media_stats(target, "MANGA")

        await ctx.send(embed=reply)


def setup(bot: commands.Bot):
    bot.add_cog(UserModule())
