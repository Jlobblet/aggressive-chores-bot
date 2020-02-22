#!usr/bin/env python3
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.sql_tools import run_file_format
from utils.user import check_user
from utils.messages import send_chore_message, parse_message


class Chores(commands.Cog):
    @commands.command(
        name=NAMES["add_chore"],
        help=HELPTEXT["add_chore"]["help"],
        brief=HELPTEXT["add_chore"]["brief"],
    )
    async def add_chore(self, ctx: Context, member: discord.Member, *message):
        check_user(ctx.guild.id, member.id)
        message_data = parse_message(message)
        if not message_data:
            await ctx.message.add_reaction("❓")
            return False
        else:
            description, parsed_time = message_data
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
