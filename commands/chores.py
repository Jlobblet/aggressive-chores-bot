#!usr/bin/env python3
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.initialise import initialise
from utils.utils import run_file_format, check_user, send_chore_message


class Chores(commands.Cog):
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
            vals = run_file_format(self.CURSOR, "sql/show_guild_user.sql", **kwargs)
            if not vals:
                embed = discord.Embed(description="You have no uncompleted chores!")
                await ctx.send(embed=embed)
        elif message == "all":
            kwargs = {"guild_id": ctx.guild.id}
            vals = run_file_format(self.CURSOR, "sql/show_guild.sql", **kwargs)
            if not vals:
                embed = discord.Embed(
                    description="There are no uncomplete chores on the server!"
                )
                await ctx.send(embed=embed)
        else:
            return None
        for v in vals:
            print(v)
            await send_chore_message(
                self.DATABASE, self.CURSOR, self.bot, ctx, ctx.guild.id, v[0]
            )
        await ctx.message.delete()

    @commands.command(
        name=NAMES["add_chore"],
        help=HELPTEXT["add_chore"]["help"],
        brief=HELPTEXT["add_chore"]["brief"],
    )
    async def add_chore(self, ctx: Context, member: discord.Member, *description):
        check_user(self.CURSOR, ctx.guild.id, member.id)
        self.DATABASE.commit()
        description = " ".join(description)
        chore_id = run_file_format(
            self.CURSOR, "sql/fetch_number_chores.sql", guild_id=ctx.guild.id
        )
        if not chore_id[0][0]:
            chore_id = 1
        else:
            chore_id = chore_id[0][0] + 1
        kwargs = {
            "user_id": member.id,
            "creator": ctx.author.id,
            "guild_id": ctx.guild.id,
            "description": description,
            "assigned_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "chore_id": chore_id,
        }
        run_file_format(self.CURSOR, "sql/add_chore.sql", **kwargs)
        self.DATABASE.commit()
        await send_chore_message(
            self.DATABASE, self.CURSOR, self.bot, ctx, ctx.guild.id, chore_id
        )
        return True

    @commands.command(
        name=NAMES["remove_chore"],
        help=HELPTEXT["remove_chore"]["help"],
        brief=HELPTEXT["remove_chore"]["brief"],
    )
    async def remove_chore(self, ctx: Context, chore_id: int):
        chore_data = run_file_format(
            self.CURSOR, "sql/find_chore.sql", guild_id=ctx.guild.id, chore_id=chore_id
        )
        if not chore_data:
            await ctx.message.add_reaction("❓")
            return False
        creator = chore_data[0][2]
        invoker_admin = run_file_format(
            self.CURSOR,
            "sql/find_user.sql",
            guild_id=ctx.guild.id,
            user_id=ctx.author.id,
        )[0][3]
        if invoker_admin > 0 or creator == ctx.author.id:
            kwargs = {"guild_id": ctx.guild.id, "chore_id": chore_id}
            run_file_format(self.CURSOR, "sql/remove_chore.sql", **kwargs)
            self.DATABASE.commit()
            await ctx.message.add_reaction("✅")
            return True
        else:
            await ctx.message.add_reaction("❌")
            return False

    @commands.command(
        name=NAMES["complete_chore"],
        help=HELPTEXT["complete_chore"]["help"],
        brief=HELPTEXT["remove_chore"]["brief"],
    )
    async def complete_chore(self, ctx: Context, chore_id: int):
        invoker_id = ctx.author.id
        chore_data = run_file_format(
            self.CURSOR,
            "sql/find_incomplete_chore.sql",
            guild_id=ctx.guild.id,
            chore_id=chore_id,
        )
        if not chore_data:
            await ctx.message.add_reaction("❓")
            return False
        asignee_id = chore_data[0][1]
        if invoker_id == asignee_id:
            kwargs = {
                "guild_id": ctx.guild.id,
                "completed_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "chore_id": chore_id,
            }
            run_file_format(self.CURSOR, "sql/complete_chore.sql", **kwargs)
            self.DATABASE.commit()
            await ctx.message.add_reaction("✅")
            return True
        else:
            await ctx.message.add_reaction("❌")
            return False


def setup(bot: Bot):
    DATABASE, CURSOR = initialise()
    bot.add_cog(Chores(bot, DATABASE, CURSOR))
