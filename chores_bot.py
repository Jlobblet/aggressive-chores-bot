#!usr/bin/env python3
import discord
from discord.ext.commands import Bot

from utils.sql_tools import run_file_format
from utils.user import check_user
from utils.admin import set_admin
from utils.prefix import get_prefix
from config.CONFIG import CONFIG
from config.DISCORD import DISCORD_SECRET

prefix = CONFIG["prefix"]
extensions = [
    "commands.chores.add_chore",
    "commands.chores.complete_chore",
    "commands.chores.remove_chore",
    "commands.chores.show_chores",
    "commands.chores.assign",
    "commands.chores.reaction_listener",
    "commands.admin.manipulate_admin",
    "commands.admin.prefix",
]
bot = Bot(command_prefix=get_prefix)


@bot.event
async def on_message(message):
    if not message.author.bot:
        check_user(message.guild.id, message.author.id)
        await bot.process_commands(message)


@bot.event
async def on_ready():
    print("Logged in as {0.name} ({0.id})".format(bot.user))
    print("====================")
    print("Checking guilds...")
    guilds = bot.guilds
    owners = {g.id: g.owner.id for g in guilds}
    for g, o in owners.items():
        set_admin(g, o, 2)
    guild_ids = {g.id for g in guilds}
    existing_guilds = {r["guild_id"] for r in run_file_format("sql/select_guilds.sql")}
    missing_guilds = guild_ids - existing_guilds
    for guild in missing_guilds:
        run_file_format("sql/add_guild.sql", guild_id=guild)
    print("...done")
    await bot.change_presence(activity=discord.Game(f"{prefix}help"))


if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded extension {extension}")
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print(f"Failed to load extension {extension}\n{exc}")

    bot.run(DISCORD_SECRET["token"])
    game = discord.Game(f"{prefix}help")
