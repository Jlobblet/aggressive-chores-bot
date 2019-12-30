#!usr/bin/env python3
import discord
from discord.ext.commands import Bot

from config import CONFIG
from commands.chores import add_chore
from utils.initialise import initialise

DATABASE, CURSOR = initialise()
# extensions = ["commands.chores"]
# bot = Bot(command_prefix=CONFIG["prefix"])

add_chore(CURSOR, "1234", "5678", "test entry")
DATABASE.commit()
DATABASE.close()
