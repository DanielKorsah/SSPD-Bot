import discord
from discord.ext import commands
import common.channels as channels


class Toys(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def lewgasm(self, ctx):
        await ctx.send("https://imgur.com/a/oLKuUVY")

    @commands.command(pass_context=True)
    async def poll(self, ctx, *question):
        q = " ".join(question)
        embed = discord.Embed(
            title=q, color=0x50bdfe)
        await ctx.send(f"{ctx.message.author.mention} asks:")
        msg = await ctx.send(embed=embed)

        await msg.add_reaction(emoji=u"\U0001F1FE")
        await msg.add_reaction(emoji=u"\U0001F1F3")

        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Toys(bot))
    print("Cog Loaded: Toys")
