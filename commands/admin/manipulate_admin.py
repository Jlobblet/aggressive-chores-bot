#!usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.sql_tools import run_file_format
from utils.user import check_user


class Admin(commands.Cog):
    @commands.command(
        name=NAMES["manipulate_admin"],
        help=HELPTEXT["manipulate_admin"]["help"],
        brief=HELPTEXT["manipulate_admin"]["brief"],
    )
    async def manipulate_admin(self, ctx: Context, member: discord.Member, level: int):
        invoker_id = ctx.author.id
        guild_id = ctx.guild.id
        target_id = member.id
        check_user(guild_id, invoker_id)
        check_user(guild_id, target_id)
        invoker_details = run_file_format(
            "sql/find_user.sql", user_id=invoker_id, guild_id=guild_id
        )[0]
        target_details = run_file_format(
            "sql/find_user.sql", user_id=target_id, guild_id=guild_id
        )[0]
        invoker_admin = invoker_details["admin_level"]
        target_admin = invoker_details["admin_level"]
        if (
            invoker_admin >= 1
            and invoker_admin >= target_admin
            and 0 <= level <= invoker_admin
        ):
            run_file_format(
                "sql/set_admin.sql",
                guild_id=guild_id,
                user_id=target_id,
                admin_level=level,
            )
            await ctx.message.add_reaction("✅")
            return True
        else:
            await ctx.message.add_reaction("❌")
            return False


def setup(bot: Bot):
    bot.add_cog(Admin())
