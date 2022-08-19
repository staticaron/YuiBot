from discord.ext import commands

from helpers import search_helper
import config

class SearchModule(commands.Cog):

    """Find Group"""

    @commands.group(name="search", aliases=["find"], description="Commands for searching Anime and Manga")
    async def search_group(self, ctx:commands.Context):
        await ctx.trigger_typing()
        if ctx.subcommand_passed is None:
            return await ctx.reply(f"Please provide a valid subcommand! {config.YUI_SHY_EMOTE}")

    """Anime Search"""

    @search_group.command(name="anime", description="Returns the anime details with provided name")
    async def anime_details(self, ctx:commands.Context, *name):

        await ctx.trigger_typing()

        name = " ".join(name)

        embd = await search_helper.get_anime_details_embed(name, ctx.author)

        await ctx.send(embed=embd)

    """Manga Search"""

    @search_group.command(name="manga", description="Returns the manga details with provide name")
    async def manga_details(self, ctx:commands.Context, *name):

        await ctx.trigger_typing()

        name = " ".join(name)

        embd = await search_helper.get_manga_details_embed(name, ctx.author)

        await ctx.send(embed=embd)

    """Character Search"""

    @search_group.command(name="character", aliases=["char"], description="Returns the character details for the character with provided name")
    async def character_details(self, ctx:commands.Context, *name):

        await ctx.trigger_typing()

        name = " ".join(name)

        embd = await search_helper.get_character_details_embed(name, ctx.author)

        await ctx.reply(embed=embd)

    """Studio Search"""

    @search_group.command(name="studio", description="Returns the studio details with provided name")
    async def studio_details(self, ctx:commands.Context, *name):

        await ctx.trigger_typing()

        name = " ".join(name)

        embd = await search_helper.get_studio_details_embed(name)

        await ctx.send(embed=embd)

def setup(bot:commands.Bot):
    bot.add_cog(SearchModule())