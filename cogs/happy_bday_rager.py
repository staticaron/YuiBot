from discord.ext import commands
from discord import TextChannel
from discord.ext import tasks

class BDay(commands.Cog):

    presence_change_time = 5

    count = 0

    bot : commands.Bot = None
    channel:TextChannel = None

    def __init__(self, bot) -> None:
        self.bot = bot
        self.channel = self.bot.get_channel(954353886632751176)
        self.update_presence.start()

    def cog_unload(self):
        self.update_presence.cancel()

    """For changing Presence"""

    @tasks.loop(seconds=presence_change_time)
    async def update_presence(self):
        await self.set_presence()  

    @update_presence.before_loop
    async def waiter(self):
        await self.bot.wait_until_ready()

    async def set_presence(self):
        
        self.channel.send("A very Happy Birthday from your cute Yui-chan <@926194062590099466>!!!!")

        self.count = self.count + 1

        if self.count == 100:
            self.presence_change_time = 15

            self.update_presence.change_interval(seconds=15)

def setup(bot):
    bot.add_cog(BDay(bot))