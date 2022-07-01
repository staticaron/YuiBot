from discord.ext import commands

from helpers import search_helper
import config

class SearchModule(commands.Cog):

    @commands.group(name="search", aliases=["find"], description="Commands for searching Anime and Manga")
    async def search_group(self, ctx:commands.Context):
        if ctx.subcommand_passed is None:
            return await ctx.reply(f"Please provide a valid subcommand! {config.YUI_SHY_EMOTE}")

    @search_group.command(name="anime", description="Returns the anime details with provided name")
    async def anime_details(self, ctx:commands.Context, *name):

        name = " ".join(name)

        embd = await search_helper.get_anime_details_embed(name)

        await ctx.send(embed=embd)

    @search_group.command(name="manga", description="Returns the manga details with provide name")
    async def manga_details(self, ctx:commands.Context, *name):

        name = " ".join(name)

        embd = await search_helper.get_manga_details_embed(name)

        await ctx.send(embed=embd)

    @search_group.command(name="character", description="Returns the character details for the character with provided name")
    async def character_details(self, ctx:commands.Context, *name):

        name = " ".join(name)

        embd = await search_helper.get_character_details_embed(name)

        await ctx.reply(embed=embd)

def setup(bot:commands.Bot):
    bot.add_cog(SearchModule())