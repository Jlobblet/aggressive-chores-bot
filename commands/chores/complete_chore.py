#!usr/bin/env python3
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from commands.chores.subcommands.complete_chore import complete_chore
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
    async def _complete_chore(self, ctx: Context, chore_id: int):
        await complete_chore(ctx, ctx.author.id, chore_id)


def setup(bot: Bot):
    bot.add_cog(Chores(bot))
