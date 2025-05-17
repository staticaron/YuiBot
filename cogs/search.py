from discord.ext import commands
from discord import Embed
from discord import Interaction

from views import warning_view, media_info_view
from managers import cache_manager
from helpers import search_helper, general_helper
import config


class SearchModule(commands.Cog):
    """Find Group"""

    @commands.group(name="search", aliases=["find"], description="Commands for searching Anime and Manga")
    @general_helper.short_cooldown()
    @general_helper.with_typing_ctx()
    async def search_group(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            return await ctx.reply(f"Please provide a valid subcommand! {config.YUI_SHY_EMOTE}")

    """Anime Search"""

    @search_group.command(name="anime", description="Returns the anime details with provided name")
    @general_helper.with_typing_ctx()
    async def anime_details(self, ctx: commands.Context, *name):
        name = " ".join(name)

        result = await search_helper.get_anime_details_embed(name, ctx.author)

        info_view = media_info_view.MediaInfoView(result["embeds"])

        if result.get("isAdult") is False:
            return await ctx.send(embed=result["embeds"]["details"], view=info_view)

        async def proceed_callback(interaction: Interaction):
            return await interaction.followup.send(embed=result["embeds"]["details"], ephemeral=True, view=info_view)

        confirmation_embd = Embed(title="Watch Out!", description="This media entry is marked as **18+**.")
        confirmation_view = warning_view.WarningView(proceed_callback)

        await ctx.send(embed=confirmation_embd, view=confirmation_view)

    """Manga Search"""

    @search_group.command(name="manga", description="Returns the manga details with provide name")
    @general_helper.with_typing_ctx()
    async def manga_details(self, ctx: commands.Context, *name):
        name = " ".join(name)

        result = await search_helper.get_manga_details_embed(name, ctx.author)

        if result.get("isAdult") is False:
            return await ctx.send(embed=result["embed"])

        async def proceed_callback(interaction: Interaction):
            return await interaction.followup.send(embed=result["embed"], ephemeral=True)

        confirmation_embd = Embed(title="Watch Out!", description="This media entry is marked as **18+**.")
        confirmation_view = warning_view.WarningView(proceed_callback)

        await ctx.send(embed=confirmation_embd, view=confirmation_view)

    """Character Search"""

    @search_group.command(name="character", aliases=["char"], description="Returns the character details for the character with provided name")
    @general_helper.with_typing_ctx()
    async def character_details(self, ctx: commands.Context, *name):
        name = " ".join(name)

        embd = await search_helper.get_character_details_embed(name, ctx.author)

        await ctx.reply(embed=embd)

    """Studio Search"""

    @search_group.command(name="studio", description="Returns the studio details with provided name")
    @general_helper.with_typing_ctx()
    async def studio_details(self, ctx: commands.Context, *name):
        name = " ".join(name)

        embd = await search_helper.get_studio_details_embed(name)

        await ctx.send(embed=embd)

    """Top ANIME By Genre"""

    @search_group.command(name="topanime", aliases=["ta"], description="Returns the top anime from a particular genre")
    @general_helper.with_typing_ctx()
    async def top_genre_anime(self, ctx: commands.Context, *genres):
        for genre in genres:
            if genre.lower() not in config.ALL_GENRE:
                return await ctx.reply(embed=cache_manager.CACHED_GENRE_EMBED)

        scroller = await search_helper.get_top_by_genre(genres, "ANIME")

        await scroller.send(ctx)

    """Top MANGA by genre"""

    @search_group.command(name="topmanga", aliases=["tm"], description="Returns the top manga from a particular genre")
    @general_helper.with_typing_ctx()
    async def top_genre_manga(self, ctx: commands.Context, *genres):
        for genre in genres:
            if genre.lower() not in config.ALL_GENRE:
                return await ctx.reply(embed=cache_manager.CACHED_GENRE_EMBED)

        scroller = await search_helper.get_top_by_genre(genres, "MANGA")

        await scroller.send(ctx)


def setup(bot: commands.Bot):
    bot.add_cog(SearchModule())
