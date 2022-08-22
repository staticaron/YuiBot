from discord.ext import commands

import config


class UtilityModule(commands.Cog):

    @commands.command(name="hello", aliases=["hi", "hola", "konnichiwa", "sup", "ping"], description="Returns Bot's Latency")
    async def latency(self, ctx: commands.Context):

        await ctx.trigger_typing()
        await ctx.reply(f"Hello **{ctx.author.name}** {config.YUI_SHY_EMOTE} - took **{round(ctx.bot.latency * 1000, 2)} ms**")

    @commands.command(name="invite", description="Returns an invite link for the bot.")
    async def invite(self, ctx: commands.Context):

        await ctx.trigger_typing()
        await ctx.reply(f"Invite Yui with this link : {config.INVITE}")


def setup(bot: commands.Bot):
    bot.add_cog(UtilityModule())
