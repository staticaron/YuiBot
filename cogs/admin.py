from discord.ext import commands

class AdminModule(commands.Cog):

    @commands.is_owner()
    @commands.command(name="disable", description="Disables a command.")
    async def disable_cmd(self, ctx:commands.Context, cmd_name:str):

        await ctx.trigger_typing()

        bot:commands.Bot = ctx.bot

        try:
            cmd:commands.Command = bot.get_command(cmd_name)
        except Exception as e:
            await ctx.reply("ERROR : {}".format(e))
        else:

            cmd.update(enabled=False)

            await ctx.send("**{}** was disabled.".format(cmd.name))

    @commands.is_owner()
    @commands.command(name="enable", description="Enables a command.")
    async def enable_cmd(self, ctx:commands.Context, cmd_name:str):

        await ctx.trigger_typing()

        bot:commands.Bot = ctx.bot

        try:
            cmd:commands.Command = bot.get_command(cmd_name)
        except Exception as e:
            await ctx.reply("ERROR : {}".format(e))
        else:

            cmd.update(enabled=True)

            await ctx.send("**{}** was enabled.".format(cmd.name))

def setup(bot:commands.Bot):
    bot.add_cog(AdminModule())