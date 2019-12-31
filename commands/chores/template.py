#!usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.initialise import initialise
from utils.utils import run_file_format, check_user, send_chore_message


class Chores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot: Bot):
    bot.add_cog(Chores(bot))
