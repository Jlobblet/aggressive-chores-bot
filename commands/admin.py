#!usr/bin/env python3
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.initialise import initialise
from utils.utils import run_file_format


class Commands(commands.Cog):
    def __init__(self, bot, DATABASE, CURSOR):
        self.bot = bot
        self.DATABASE = DATABASE
        self.CURSOR = CURSOR

    @commands.command(
        name=NAMES["manipulate_admin"],
        help=HELPTEXT["manipulate_admin"]["help"],
        brief=HELPTEXT["manipulate_admin"]["brief"],
    )
    async def manipulate_admin(self, ctx: Context, member: discord.Member, level: int):
        invoker_id = ctx.author.id
        guild_id = ctx.guild.id
        target_id = member.id
        invoker_details = run_file_format(
            self.CURSOR, "sql/find_user.sql", user_id=invoker_id, guild_id=guild_id
        )[0]
        target_details = run_file_format(
            self.CURSOR, "sql/find_user.sql", user_id=target_id, guild_id=guild_id
        )[0]
        print(invoker_details)
        print(target_details)
        invoker_admin = invoker_details[3]
        target_admin = invoker_details[3]
        if (
            invoker_admin >= 1
            and invoker_admin >= target_admin
            and 0 <= level <= invoker_admin
        ):
            run_file_format(
                self.CURSOR,
                "sql/set_admin.sql",
                guild_id=guild_id,
                user_id=target_id,
                admin_level=level,
            )
            self.DATABASE.commit()
        else:
            pass


def setup(bot: Bot):
    DATABASE, CURSOR = initialise()
    bot.add_cog(Commands(bot, DATABASE, CURSOR))
