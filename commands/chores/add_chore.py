#!usr/bin/env python3
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.utils import run_file_format, check_user, send_chore_message
from utils.parse_time import parse_time


class Chores(commands.Cog):
    @commands.command(
        name=NAMES["add_chore"],
        help=HELPTEXT["add_chore"]["help"],
        brief=HELPTEXT["add_chore"]["brief"],
    )
    async def add_chore(self, ctx: Context, member: discord.Member, deadline=None, *description):
        check_user(ctx.guild.id, member.id)
        description = " ".join(description)
        if not description and not deadline:
            await ctx.message.add_reaction("❓")
            return False
        parsed_time = parse_time(deadline)
        if not parsed_time:
            description = "{} {}".format(deadline, description)
            parsed_time = "NULL"
        else:
            parsed_time = f"\"{parsed_time}\""
        chore_id = run_file_format("sql/fetch_number_chores.sql", guild_id=ctx.guild.id)
        print(chore_id)
        if chore_id and not chore_id[0]["max_chore_id"]:
            chore_id = 1
        else:
            chore_id = chore_id[0]["max_chore_id"] + 1
        kwargs = {
            "user_id": member.id,
            "creator": ctx.author.id,
            "guild_id": ctx.guild.id,
            "description": description,
            "assigned_date": datetime.datetime.now(),
            "chore_id": chore_id,
            "deadline": parsed_time,
        }
        run_file_format("sql/add_chore.sql", **kwargs)
        await send_chore_message(ctx.bot, ctx, ctx.guild.id, chore_id)
        return True


def setup(bot: Bot):
    bot.add_cog(Chores())
