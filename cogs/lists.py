from discord.ext import commands

from helpers import general_helper, lists_helper
import config

class ListsModule(commands.Cog):

    @commands.group(name="add")
    async def add_group(self, ctx:commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.reply("Please provide a valid subcommand {}".format(config.YUI_SHY_EMOTE))
            return

    @add_group.command(name="ptw", aliases=["planning"], case_insensitive=True, description="Adds anime to your planning to watch list")
    @commands.check(general_helper.validate_user)
    async def ptw(self,ctx:commands.Context, *anime):
        anime = " ".join(anime)

        await lists_helper.add_ptw(anime)
        

def setup(bot:commands.Bot):
    bot.add_cog(ListsModule())