import discord
from discord.ext import commands
import common.channels as channels


class Debugging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Moderators™")
    async def ping(self, ctx):
        await ctx.send("pong!")

    @commands.command(pass_context=True)
    @commands.has_role("Moderators™")
    async def channelTest(self, ctx, flag: int):
        if flag == 3:
            await channels.general.send("test" + str(flag))
        elif flag == 2:
            await channels.modChannel.send("test" + str(flag))
        elif flag == 1:
            await channels.logChannel.send("test" + str(flag))
        else:
            ctx.send("Incrrect usage. \n channeltest [x] where 0<x<4")

    @commands.command(pass_context=True)
    @commands.has_role("Moderators™")
    async def pmTest(self, ctx, user: discord.Member, *message: str):
        await user.send(message)


def setup(bot):
    bot.add_cog(Debugging(bot))
    print("Cog Loaded: Debugging")
