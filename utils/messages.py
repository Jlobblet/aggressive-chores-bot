#!usr/bin/env python3
import datetime

import discord

from utils.sql_tools import run_file_format
from utils.parse_time import parse_time


async def del_messages(bot, guild_id, chore_id):
    messages = run_file_format("sql/find_message_chore.sql", chore_id=chore_id)
    del_dict = {m["message_id"]: m["channel_id"] for m in messages}
    for m_id, c_id in del_dict.items():
        channel = bot.get_channel(c_id)
        if channel:
            msg = await channel.fetch_message(m_id)
            await msg.delete()
    run_file_format("sql/delete_messages.sql", chore_id=chore_id)


async def qmark(message, emoji="❓"):
    await message.add_reaction(emoji)


async def send_chore_message(bot, ctx, guild_id, chore_id):
    chore_data = run_file_format(
        "sql/find_chore.sql", guild_id=guild_id, chore_id=chore_id
    )
    if not chore_data:
        return None
    chore_data = chore_data[0]
    guild_id = chore_data["guild_id"]
    user_id = chore_data["user_id"]
    description = chore_data["description"]
    assigned_date = chore_data["assigned_date"]
    deadline = chore_data["deadline"]
    member = bot.get_guild(guild_id).get_member(user_id)
    if member is not None:
        username = member.display_name
        url = member.avatar_url
    else:
        username = "Unknown"
        url = ""
    embed = discord.Embed(title=username, description=description)
    if deadline and deadline < datetime.datetime.now():
        embed.colour = discord.Colour.red()
    embed.set_thumbnail(url=url)
    embed.set_footer(text=f"id {chore_id} created at {assigned_date}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")
    await msg.add_reaction("🗑️")
    kwargs = {
        "message_id": msg.id,
        "channel_id": msg.channel.id,
        "chore_id": chore_id,
        "creation_time": datetime.datetime.now().strftime("%Y-%m-%-d %H:%M:%S"),
    }
    run_file_format("sql/add_message.sql", **kwargs)


def parse_message(message):
    if len(message) == 0:
        return None
    if len(message) == 1:
        description = message[0]
        parsed_time = "NULL"
    elif len(message) > 1:
        deadline = message[0]
        description = " ".join(message[1:])
        if not description and not deadline:
            return False
        parsed_time = parse_time(deadline)
        if not parsed_time:
            description = f"{deadline} {description}"
            parsed_time = "NULL"
        else:
            parsed_time = f'"{parsed_time}"'
    return description, parsed_time
