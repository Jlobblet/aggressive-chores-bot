#!usr/bin/env python3
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from commands.chores.shared.complete_chore import complete_chore
from utils.utils import run_file_format, check_admin, del_messages



class Chores(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener(name="on_reaction_add")
    async def on_reaction_add(self, reaction, user):
        if not user.bot:
            message_id = reaction.message.id
            channel_id = reaction.message.channel.id
            guild_id = reaction.message.guild.id
            message_data = run_file_format(
                "sql/find_message.sql", message_id=message_id, channel_id=channel_id
            )
            chore_id = message_data[0]["chore_id"]
            chore_data = run_file_format(
                "sql/find_chore.sql", guild_id=guild_id, chore_id=chore_id
            )[0]
            asignee_id = chore_data["user_id"]
            creator_id = chore_data["creator"]
            if reaction.emoji == "✅" and user.id == asignee_id:
                await complete_chore(reaction, user.id, chore_id)
            elif reaction.emoji == "🗑️" and (
                check_admin(user.id, reaction.message.guild.id) or creator_id == user.id
            ):
                run_file_format(
                    "sql/remove_chore.sql", guild_id=guild_id, chore_id=chore_id
                )
            else:
                return None
            await del_messages(self.bot, guild_id, chore_id)

def setup(bot: Bot):
    bot.add_cog(Chores(bot))

