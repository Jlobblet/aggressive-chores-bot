from discord.ext import commands
from discord.ext.commands import Bot

from utils.sql_tools import run_file_format


def get_prefix(bot: Bot, message):
    prefix = run_file_format("sql/get_prefix.sql", guild_id=message.guild.id)[0][
        "prefix"
    ]
    return commands.when_mentioned_or(prefix)(bot, message)
