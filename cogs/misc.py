from discord.ext import commands

from helpers import misc_helper

class MiscModule(commands.Cog):

    @commands.command(name="quote", description="Returns a random anime quote")
    @commands.cooldown(rate=5, per=30*60, type=commands.BucketType.user)
    async def anime_quote(self, ctx:commands.Context):
        reply = await misc_helper.get_random_anime_quote_embed()

        await ctx.send(embed=reply)

    @commands.command(name="pfp", aliases=["profile_pic", "picture", "waifu"], description="Returns a random waifu.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def waifu(self, ctx:commands.Context):
        reply = await misc_helper.get_waifu_embed()

        await ctx.send(embed=reply)

def setup(bot):
    bot.add_cog(MiscModule())