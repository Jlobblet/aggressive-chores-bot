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
        name=NAMES["show_chores"],
        help=HELPTEXT["show_chores"]["help"],
        brief=HELPTEXT["show_chores"]["brief"],
    )
    async def show_chores(self, ctx: Context, message):
        if message == "my":
            kwargs = {"guild_id": ctx.guild.id, "user_id": ctx.author.id}
            vals = run_file_format(
                self.CURSOR, "utils/sql/show_guild_user.sql", **kwargs
            )
        elif message == "all":
            kwargs = {"guild_id": ctx.guild.id}
            vals = run_file_format(self.CURSOR, "utils/sql/show_guild.sql", **kwargs)
        else:
            return None
        for i, v in enumerate(vals):
            member = ctx.guild.get_member(int(v[1]))
            if member is not None:
                username = member.display_name
                url = member.avatar_url
            else:
                username = "Unknown"
                url = ""
            embed = discord.Embed(title=username, description=v[3])
            embed.set_thumbnail(url=url)
            embed.set_footer(text=f"id {v[0]} created at {v[4]}")
            await ctx.send(embed=embed)

    @commands.command(
        name=NAMES["add_chore"],
        help=HELPTEXT["add_chore"]["help"],
        brief=HELPTEXT["add_chore"]["brief"],
    )
    async def add_chore(self, ctx: Context, member: discord.Member, *description):
        description = " ".join(description)
        kwargs = {
            "user_id": member.id,
            "guild_id": ctx.guild.id,
            "description": description,
            "assigned_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        run_file_format(self.CURSOR, "utils/sql/add_chore.sql", **kwargs)
        self.DATABASE.commit()
        await ctx.message.add_reaction("✅")
        return True

    @commands.command(
        name=NAMES["remove_chore"],
        help=HELPTEXT["remove_chore"]["help"],
        brief=HELPTEXT["remove_chore"]["brief"],
    )
    async def remove_chore(self, ctx: Context, chore_id: int):
        kwargs = {"chore_id": chore_id, "guild_id": ctx.guild.id}
        run_file_format(self.CURSOR, "utils/sql/remove_chore.sql", **kwargs)
        self.DATABASE.commit()
        await ctx.message.add_reaction("✅")
        return True

    @commands.command(
        name=NAMES["complete_chore"],
        help=HELPTEXT["complete_chore"]["help"],
        brief=HELPTEXT["remove_chore"]["brief"],
    )
    async def complete_chore(self, ctx: Context, chore_id: int):
        kwargs = {
            "completed_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "chore_id": chore_id,
            "guild_id": ctx.guild.id,
        }
        run_file_format(self.CURSOR, "utils/sql/complete_chore.sql", **kwargs)
        self.DATABASE.commit()
        await ctx.message.add_reaction("✅")
        return True


def setup(bot: Bot):
    DATABASE, CURSOR = initialise()
    bot.add_cog(Commands(bot, DATABASE, CURSOR))
