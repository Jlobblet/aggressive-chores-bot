#!usr/bin/env python3
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.utils import run_file_format
from utils.initialise import initialise

DATABASE, CURSOR = initialise()


class Commands(commands.Cog):
    @commands.command(
        name=NAMES["show_chores"],
        help=HELPTEXT["show_chores"]["help"],
        brief=HELPTEXT["show_chores"]["brief"],
    )
    async def show_chores(self, ctx: Context, message):
        await ctx.send(message)
        # if not user_id:
        #     kwargs = {"guild_id": guild_id}
        #     run_file_format(
        #         CURSOR, "utils/sql/show_guild.sql", **kwargs
        #     )
        # else:
        #     kwargs = {"guild_id": guild_id, "user_id": user_id}
        #     run_file_format(
        #         CURSOR, "utils/sql/show_guild_user.sql", **kwargs
        #     )

    @commands.command(
        name=NAMES["add_chore"],
        help=HELPTEXT["add_chore"]["help"],
        brief=HELPTEXT["add_chore"]["brief"],
    )
    async def add_chore(self, ctx: Context, member: discord.Member, description):
        message = f"Added chore *{description}* for {member.display_name}"
        await ctx.send(message)
        kwargs = {
            "user_id": member.id,
            "guild_id": ctx.guild.id,
            "description": description,
            "assigned_date": datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
        run_file_format(CURSOR, "utils/sql/add_chore.sql", **kwargs)
        DATABASE.commit()
        return True


def setup(bot: Bot):
    bot.add_cog(Commands(bot))
