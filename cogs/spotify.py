from discord.ext import commands

from helpers import general_helper
from managers import cache_manager as cm


class SpotifyModule(commands.Cog):
    @commands.group(
        name="spotify",
        description="Group containing all the spotify module related commands",
    )
    @commands.has_permissions(administrator=True)
    async def spotify(self, ctx: commands.Context):
        if ctx.guild is None:
            return

        if ctx.subcommand_passed is None:
            current_server = await cm.manager.get_server(
                ctx.guild.id, True, ctx.guild.name
            )
            if current_server is None:
                await ctx.reply(
                    "Server Not Found! Looks like you can't use this command in this server"
                )
                return

            enabled = current_server.get("spotify", {}).get("enabled", False)

            await cm.manager.update_server(
                ctx.guild.id, {"spotify": {"enabled": not enabled}}
            )

            await ctx.send(
                "Spotify Module status set to "
                + ("offline" if enabled is True else "online")
            )

    @spotify.command(
        "style",
        description="Change the style of the spotify alternate music detection. [embed/text]",
    )
    @commands.has_permissions(administrator=True)
    @general_helper.with_typing_ctx()
    async def style(self, ctx: commands.Context, style: str):
        if ctx.guild is None:
            return

        if style not in ["embed", "text"]:
            return await ctx.send("Wrong Style type. Please pick [embed/text]")

        current_server = await cm.manager.get_server(ctx.guild.id, True, ctx.guild.name)
        if current_server is None:
            await ctx.reply(
                "Server Not Found! Maybe you can't use this command in this server"
            )
            return

        current_style = current_server.get("spotify", {}).get("style", "text")

        if current_style == style:
            return await ctx.send(
                "Spotify Module Style already set to " + current_style
            )

        await cm.manager.update_server(ctx.guild.id, {"spotify": {"style": style}})

        await ctx.send("Spotify Module Style set to " + style)


def setup(bot: commands.Bot):
    bot.add_cog(SpotifyModule())
