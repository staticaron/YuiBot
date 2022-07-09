from discord.ext import commands

from helpers import anime_helper

class AnimeModule(commands.Cog):

    @commands.command(name="quote", description="Returns a random anime quote")
    @commands.cooldown(rate=5, per=30*60, type=commands.BucketType.user)
    async def anime_quote(self, ctx:commands.Context):
        reply = await anime_helper.get_random_anime_quote_embed()

        await ctx.send(embed=reply)

def setup(bot):
    bot.add_cog(AnimeModule())