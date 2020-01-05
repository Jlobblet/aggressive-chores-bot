#!usr/bin/env python3
import discord
from discord.ext import commands
from discord.ext.commands import Bot

from config.HELPTEXT import HELPTEXT
from config.NAMES import NAMES
from utils.utils import run_file_format


class Chores(commands.Cog):
    pass


def setup(bot: Bot):
    bot.add_cog(Chores())
