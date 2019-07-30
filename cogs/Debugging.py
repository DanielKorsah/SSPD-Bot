import discord
from discord.ext import commands


class Debugging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        for com in self.get_commands():
            print(com)
        for lis in self.get_listeners():
            print(lis)

    @commands.command()
    @commands.has_role("Moderators™")
    async def ping(self, ctx):
        await ctx.send("pong!")


def setup(bot):
    bot.add_cog(Debugging(bot))
    print("Cog Loaded: Debugging")
