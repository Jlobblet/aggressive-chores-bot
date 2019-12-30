#!usr/bin/env python3
import discord
from discord.ext.commands import Bot

from config import CONFIG
from utils.utils import run_from_file

extensions = ["commands.chores"]
bot = Bot(command_prefix=CONFIG["prefix"])
