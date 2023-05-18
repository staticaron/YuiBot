from discord.ext import commands

from helpers import pixiv_helper

class PixivModule(commands.Cog):

    @commands.group(name="pixiv", description="A bunch of commands related to pixiv.")
    async def pixiv(self, ctx:commands.Context):
        if ctx.subcommand_passed == None:
            return await ctx.reply("Please provide a valid subcommand")
        
    @pixiv.command(name="search", description="Returns images from pixiv")
    async def search(self, ctx:commands.Context, value:str):

        search_embed = await pixiv_helper.search_embed(value)

        await ctx.send(embed=search_embed)


def setup(bot:commands.Bot):
    bot.add_cog(PixivModule())