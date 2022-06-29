from discord.ext import commands

from helpers import anime_helper

class AnimeDataModule(commands.Cog):

    @commands.command(name="anime", description="Returns the anime details with provided name")
    async def anime_details(self, ctx:commands.Context, *name):

        name = " ".join(name)

        embd = await anime_helper.get_anime_details_embed(name)

        await ctx.reply(embed=embd)

def setup(bot:commands.Bot):
    bot.add_cog(AnimeDataModule())