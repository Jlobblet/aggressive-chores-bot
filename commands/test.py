import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context


class Chores(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="ping", help="Pong!", brief="Pong!")
    async def ping(self, ctx: Context):
        await ctx.send("Pong!")


def setup(bot: Bot):
    bot.add_cog(Chores(bot))
