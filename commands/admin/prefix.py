#!usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.utils import run_file_format


class Admin(commands.Cog):
    @commands.command(
        name=NAMES["change_prefix"],
        help=HELPTEXT["change_prefix"]["help"],
        brief=HELPTEXT["change_prefix"]["brief"],
    )
    @commands.is_owner()
    async def change_prefix(self, ctx, new_pre):
        if len(new_pre) != 1:
            await ctx.send(
                embed=discord.Embed(
                    description="Prefixes must be length 1!",
                    colour=discord.Colour.red(),
                )
            )
        else:
            run_file_format("sql/set_prefix.sql", guild_id=ctx.guild.id, prefix=new_pre)
            await ctx.message.add_reaction("✅")


def setup(bot: Bot):
    bot.add_cog(Admin())
