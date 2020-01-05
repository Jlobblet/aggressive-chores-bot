#!usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.utils import run_file_format, check_admin


class Chores(commands.Cog):
    @commands.command(
        name=NAMES["remove_chore"],
        help=HELPTEXT["remove_chore"]["help"],
        brief=HELPTEXT["remove_chore"]["brief"],
    )
    async def remove_chore(self, ctx: Context, chore_id: int):
        chore_data = run_file_format(
            "sql/find_chore.sql", guild_id=ctx.guild.id, chore_id=chore_id
        )
        if not chore_data:
            await ctx.message.add_reaction("❓")
            return False
        creator = chore_data[0]["creator"]
        if check_admin(ctx.author.id, ctx.guild.id) or creator == ctx.author.id:
            kwargs = {"guild_id": ctx.guild.id, "chore_id": chore_id}
            run_file_format("sql/remove_chore.sql", **kwargs)
            await ctx.message.add_reaction("✅")
            return True
        else:
            await ctx.message.add_reaction("❌")
            return False


def setup(bot: Bot):
    bot.add_cog(Chores())
