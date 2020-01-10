#!usr/bin/env python3
from discord.ext import commands
from discord.ext.commands import Bot, Context

from commands.chores.shared.complete_chore import complete_chore
from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES


class Chores(commands.Cog):
    @commands.command(
        name=NAMES["complete_chore"],
        help=HELPTEXT["complete_chore"]["help"],
        brief=HELPTEXT["remove_chore"]["brief"],
    )
    async def _complete_chore(self, ctx: Context, chore_id: int):
        await complete_chore(ctx, ctx.author.id, chore_id)


def setup(bot: Bot):
    bot.add_cog(Chores())
