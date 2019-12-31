#!usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.utils import run_file_format, send_chore_message


class Chores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name=NAMES["show_chores"],
        help=HELPTEXT["show_chores"]["help"],
        brief=HELPTEXT["show_chores"]["brief"],
    )
    async def show_chores(self, ctx: Context, message):
        if message == "my":
            kwargs = {"guild_id": ctx.guild.id, "user_id": ctx.author.id}
            vals = run_file_format("sql/show_guild_user.sql", **kwargs)
            if not vals:
                embed = discord.Embed(description="You have no uncompleted chores!")
                await ctx.send(embed=embed)
        elif message == "all":
            kwargs = {"guild_id": ctx.guild.id}
            vals = run_file_format("sql/show_guild.sql", **kwargs)
            if not vals:
                embed = discord.Embed(
                    description="There are no uncomplete chores on the server!"
                )
                await ctx.send(embed=embed)
        else:
            return None
        for v in vals:
            await send_chore_message(self.bot, ctx, ctx.guild.id, v["chore_id"])
        await ctx.message.delete()


def setup(bot: Bot):
    bot.add_cog(Chores(bot))
