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
from config.CONFIG import CONFIG
from config.DISCORD import DISCORD_SECRET

extensions = ["commands.chores", "commands.admin"]
bot = Bot(command_prefix=CONFIG["prefix"])
DATABASE, CURSOR = initialise()


@bot.event
async def on_message(message):
    if not message.author.bot:
        check_user(CURSOR, message)
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
        set_admin(CURSOR, g, o, 2)
        DATABASE.commit()
    print(owners)
    guild_ids = {str(g.id) for g in guilds}
    existing_guilds = {r[0] for r in run_file_format(CURSOR, "sql/select_guilds.sql")}
    missing_guilds = guild_ids - existing_guilds
    for guild in missing_guilds:
        run_file_format(CURSOR, "sql/add_guild.sql", guild_id=guild)
        DATABASE.commit()
    print("...done")


@bot.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        message_id = reaction.message.id
        chore_id = run_file_format(
            CURSOR, "sql/find_message.sql", message_id=message_id
        )[0][3]
        asignee_id = run_file_format(CURSOR, "sql/find_chore.sql", chore_id=chore_id)[
            0
        ][1]
        if reaction.emoji == "✅" and str(user.id) == asignee_id:
            kwargs = {
                "completed_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "chore_id": chore_id,
            }
            run_file_format(CURSOR, "sql/complete_chore.sql", **kwargs)
        elif reaction.emoji == "🗑️" and check_admin(
            CURSOR, user.id, reaction.message.guild.id
        ):
            run_file_format(CURSOR, "sql/remove_chore.sql", chore_id=chore_id)
        await del_messages(CURSOR, bot, chore_id)
        DATABASE.commit()


if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load extension {}\n{}".format(extension, exc))

    bot.run(DISCORD_SECRET["token"])
