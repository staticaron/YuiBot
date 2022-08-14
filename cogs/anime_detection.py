from discord.ext import commands

from helpers import anime_detection_helper

class AnimeDetection(commands.Cog):

    @commands.command(name="detect-anime", aliases=["da"], description="Returns the anime name from the provided image.")
    async def detect_anime(self, ctx:commands.Context, url):

        await ctx.trigger_typing()

        embd = await anime_detection_helper.get_embed(url)

        await ctx.reply(embed=embd)

def setup(bot:commands.Bot):
    bot.add_cog(AnimeDetection())