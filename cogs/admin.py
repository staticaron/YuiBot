from discord.ext import commands


class AdminModule(commands.Cog):
    @commands.is_owner()
    @commands.command(name="disable", description="Disables a command.")
    async def disable_cmd(self, ctx: commands.Context, cmd_name: str):

        await ctx.trigger_typing()

        bot: commands.Bot = ctx.bot

        try:
            cmd: commands.Command | None = bot.get_command(cmd_name)
            if cmd is None:
                await ctx.reply("Command not found!")
                return

        except Exception as e:  # noqa: BLE001
            await ctx.reply(f"ERROR : {e}")

        else:
            cmd.update(enabled=False)
            await ctx.send(f"**{cmd.name}** was disabled.")

    @commands.is_owner()
    @commands.command(name="enable", description="Enables a command.")
    async def enable_cmd(self, ctx: commands.Context, cmd_name: str):

        await ctx.trigger_typing()

        bot: commands.Bot = ctx.bot

        try:
            cmd: commands.Command | None = bot.get_command(cmd_name)
            if cmd is None:
                await ctx.reply("Command not found!")
                return

        except Exception as e:  # noqa: BLE001
            await ctx.reply(f"ERROR : {e}")

        else:
            cmd.update(enabled=True)
            await ctx.send(f"**{cmd.name}** was enabled.")


def setup(bot: commands.Bot):
    bot.add_cog(AdminModule())
