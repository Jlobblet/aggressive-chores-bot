#!usr/bin/env pythoin3
import discord
import datetime

from utils.initialise import initialise
from utils.teardown import teardown


def run_whole_file(filepath):
    DATABASE, CURSOR = initialise()
    with open(filepath, "r") as f:
        sql = f.read().split(";")
    for command in sql:
        if command != "\n":
            print(f"Executing\n{command}")
            CURSOR.execute(command)
            print("...done")
    DATABASE.commit()
    teardown(CURSOR, DATABASE)


def run_file_format(filepath, **kwargs):
    DATABASE, CURSOR = initialise()
    with open(filepath, "r") as f:
        sql = f.read().format(**kwargs)
    print(f"Executing\n{sql}")
    CURSOR.execute(sql)
    print("...done")
    return_list = [x for x in CURSOR]
    DATABASE.commit()
    teardown(CURSOR, DATABASE)
    return return_list


def check_user(guild_id, user_id):
    hits = run_file_format("sql/find_user.sql", user_id=user_id, guild_id=guild_id)
    if not hits:
        run_file_format(
            "sql/add_user.sql", user_id=user_id, guild_id=guild_id,
        )


def set_admin(guild_id, user_id, admin_level):
    check_user(guild_id, user_id)
    run_file_format(
        "sql/set_admin.sql",
        guild_id=guild_id,
        user_id=user_id,
        admin_level=admin_level,
    )


def check_admin(user_id, guild_id, min_admin_level=1):
    check_user(guild_id, user_id)
    hits = run_file_format("sql/find_user.sql", user_id=user_id, guild_id=guild_id)
    print(hits)
    admin_level = hits[0]["admin_level"]
    if admin_level >= min_admin_level:
        return True
    else:
        return False


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
