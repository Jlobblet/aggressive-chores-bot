#!usr/bin/env python3
from discord.ext.commands import Bot

from config import CONFIG
from config.DISCORD import DISCORD_SECRET
from utils.initialise import initialise

DATABASE, CURSOR = initialise()
extensions = ["commands.chores"]
bot = Bot(command_prefix=CONFIG["prefix"])


@bot.event
async def on_message(message):
    if not message.author.bot:
        await bot.process_commands(message)


@bot.event
async def on_ready():
    print("Logged in as {0.name} ({0.id})".format(bot.user))
    print("====================")
    print("Checking guilds...")
    guilds = bot.guids()
    print(guilds)
    print("...done")


if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print(
                "Failed to load extension {}\n{}".format(extension, exc)
            )

    bot.run(DISCORD_SECRET["token"])
DATABASE.close()
