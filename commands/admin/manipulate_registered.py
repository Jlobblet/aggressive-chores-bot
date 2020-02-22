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
        name=NAMES["register"],
        help=HELPTEXT["register"]["help"],
        brief=HELPTEXT["register"]["brief"],
    )
    async def register(self, ctx: Context, *args):
        guild_id = ctx.guild.id
        if ctx.message.mentions:
            for member in ctx.message.mentions:
                target_id = member.id
                check_user(guild_id, target_id)
                run_file_format(
                    "sql/set_registered.sql",
                    guild_id=guild_id,
                    user_id=target_id,
                    registered=1,
                )
        else:
            check_user(guild_id, ctx.message.author.id)
            run_file_format(
                "sql/set_registered.sql",
                guild_id=guild_id,
                user_id=ctx.message.author.id,
                registered=1,
            )
        await ctx.message.add_reaction("✅")
        return True

    @commands.command(
        name=NAMES["deregister"],
        help=HELPTEXT["deregister"]["help"],
        brief=HELPTEXT["deregister"]["brief"],
    )
    async def deregister(self, ctx: Context, *args):

        guild_id = ctx.guild.id
        if ctx.message.mentions:
            for member in ctx.message.mentions:
                target_id = member.id
                check_user(guild_id, target_id)
                run_file_format(
                    "sql/set_registered.sql",
                    guild_id=guild_id,
                    user_id=target_id,
                    registered=0,
                )
        else:
            check_user(guild_id, ctx.message.author.id)
            run_file_format(
                "sql/set_registered.sql",
                guild_id=guild_id,
                user_id=ctx.message.author.id,
                registered=0,
            )
        await ctx.message.add_reaction("✅")
        return True


def setup(bot: Bot):
    bot.add_cog(Admin())
