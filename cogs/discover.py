from typing import Callable
from functools import wraps
import logging

from discord.ext import commands


class DiscoverModule(commands.Cog):
    def apply_filters(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self, ctx: commands.Context, *, filter_string: str):
            logging.info(len(filter_string))
            logging.info(" ".join(filter_string))

            parse_filters = {}

            await func(self, ctx, filters=parse_filters)

        return wrapper

    @commands.group(
        name="discover",
        description="Discover media list from anilist. Supports FILTERS",
    )
    async def discover_group(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            return ctx.send("Please provide a valid subcommand!")

    @discover_group.command(name="anime", description="Disover anime by filters")
    @apply_filters
    async def discover_anime(self, ctx: commands.Context, *, filters):
        logging.info(filters)


def setup(bot: commands.Bot):
    bot.add_cog(DiscoverModule())
