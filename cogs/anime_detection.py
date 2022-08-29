from discord.ext import commands
from discord import Embed

from views.scroller import Scroller
from helpers import anime_detection_helper, general_helper


class AnimeDetection(commands.Cog):

    @commands.command(name="detect-anime", aliases=["da"], description="Returns the anime name from the provided image.")
    @general_helper.long_cooldown()
    async def detect_anime(self, ctx: commands.Context, url):

        await ctx.trigger_typing()

        output = await anime_detection_helper.get_all_detected_anime_scroller(url)

        if isinstance(output, Embed):
            await ctx.reply(embed=output)
        elif isinstance(output, Scroller):
            await output.send(ctx)

def setup(bot: commands.Bot):
    bot.add_cog(AnimeDetection())
