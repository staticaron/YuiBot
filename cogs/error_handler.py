from discord.ext import commands
from discord import Embed
import traceback
import sys

from helpers import general_helper
import config


class ErrorHandlerModule(commands.Cog):

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):

        cog = ctx.cog

        if hasattr(ctx.command, "on_error"):
            return

        if cog:
            if cog._get_overridden_method(cog.cog_command_error):
                return

        ignored_exceptions = (commands.CommandNotFound, )

        error = getattr(error, 'original', error)
        if isinstance(error, ignored_exceptions):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except:
                pass

        elif isinstance(error, commands.CommandOnCooldown):
            time = int(ctx.command.get_cooldown_retry_after(ctx))
            time_str = await general_helper.get_time_str_from_seconds(time)
            await ctx.reply("You are on a cooldown. Please wait for {}".format(time_str))

        elif isinstance(error, commands.CheckFailure):
            await ctx.reply(embed=await general_helper.get_information_embed(
                title="Damn!",
                description="You are not logged in with your AniList Account. Log-in using `login` command",
                color=config.ERROR_COLOR
            ))

        else:
            embd = Embed(title="Damn",
                         color=config.ERROR_COLOR,
                         description="Error occurred while trying to run this command.",)

            embd.add_field(
                name="Details for Nerds",
                value="```{}```".format(error),
                inline=False
            )

            await ctx.reply(embed=embd)

            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandlerModule())
