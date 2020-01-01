#!usr/bin/env python3
import datetime

import discord
from discord.ext.commands import Bot

from utils.initialise import initialise
from utils.utils import (
    run_file_format,
    check_user,
    check_admin,
    set_admin,
    del_messages,
)
from commands.chores.subcommands.complete_chore import complete_chore
from config.CONFIG import CONFIG
from config.DISCORD import DISCORD_SECRET

prefix = CONFIG["prefix"]
extensions = [
    "commands.chores.add_chore",
    "commands.chores.complete_chore",
    "commands.chores.remove_chore",
    "commands.chores.show_chores",
    "commands.admin",
]
bot = Bot(command_prefix=prefix)
DATABASE, CURSOR = initialise()


@bot.event
async def on_message(message):
    if not message.author.bot:
        check_user(message.guild.id, message.author.id)
        DATABASE.commit()
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


@bot.event
async def on_reaction_add(reaction, user):
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
        await del_messages(bot, guild_id, chore_id)


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
