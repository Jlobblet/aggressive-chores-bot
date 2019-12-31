#!usr/bin/env python3
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.utils import run_file_format


class Chores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name=NAMES["complete_chore"],
        help=HELPTEXT["complete_chore"]["help"],
        brief=HELPTEXT["remove_chore"]["brief"],
    )
    async def complete_chore(self, ctx: Context, chore_id: int):
        invoker_id = ctx.author.id
        chore_data = run_file_format(
            "sql/find_incomplete_chore.sql", guild_id=ctx.guild.id, chore_id=chore_id,
        )
        if not chore_data:
            await ctx.message.add_reaction("❓")
            return False
        asignee_id = chore_data[0]["user_id"]
        if invoker_id == asignee_id:
            kwargs = {
                "guild_id": ctx.guild.id,
                "completed_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "chore_id": chore_id,
            }
            run_file_format("sql/complete_chore.sql", **kwargs)
            await ctx.message.add_reaction("✅")
            return True
        else:
            await ctx.message.add_reaction("❌")
            return False


def setup(bot: Bot):
    bot.add_cog(Chores(bot))
