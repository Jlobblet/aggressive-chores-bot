#!usr/bin/env python3
import datetime
import random

import numpy as np
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.sql_tools import run_file_format
from utils.messages import send_chore_message, parse_message


class Chores(commands.Cog):
    @commands.command(
        name=NAMES["assign_chore"],
        help=HELPTEXT["assign_chore"]["help"],
        brief=HELPTEXT["assign_chore"]["brief"],
    )
    async def assign_chore(self, ctx: Context, *message):
        message_data = parse_message(message)
        if not message_data:
            await ctx.message.add_reaction("❓")
            return False
        description, parsed_time = message_data
        potential = np.array(
            [
                x["user_id"]
                for x in run_file_format("sql/show_users.sql", guild_id=ctx.guild.id)
            ]
        )
        complete = np.array(
            [
                run_file_format(
                    "sql/count_complete.sql", guild_id=ctx.guild.id, user_id=x
                )[0]["complete_chores"]
                for x in potential
            ]
        )
        min_users = potential[complete == min(complete)]
        unlucky_sod = random.choice(min_users)
        chore_id = run_file_format("sql/fetch_number_chores.sql", guild_id=ctx.guild.id)
        print(chore_id)
        if chore_id and not chore_id[0]["max_chore_id"]:
            chore_id = 1
        else:
            chore_id = chore_id[0]["max_chore_id"] + 1
        kwargs = {
            "user_id": unlucky_sod,
            "creator": ctx.author.id,
            "guild_id": ctx.guild.id,
            "description": description,
            "assigned_date": datetime.datetime.now(),
            "chore_id": chore_id,
            "deadline": parsed_time,
        }
        run_file_format("sql/add_chore.sql", **kwargs)
        await ctx.send(f"<@{unlucky_sod}> drew the short straw!")
        await send_chore_message(ctx.bot, ctx, ctx.guild.id, chore_id)
        return True


def setup(bot: Bot):
    bot.add_cog(Chores())
