#!usr/bin/env pythoin3
import discord
import datetime


def run_whole_file(CURSOR, filepath):
    with open(filepath, "r") as f:
        sql = f.read().split(";")
    for command in sql:
        if command != "\n":
            print(f"Executing\n{command}")
            CURSOR.execute(command)
            print("...done")


def run_file_format(CURSOR, filepath, **kwargs):
    with open(filepath, "r") as f:
        sql = f.read().format(**kwargs)
    print(f"Executing\n{sql}")
    CURSOR.execute(sql)
    print("...done")
    return [x for x in CURSOR]


def check_user(CURSOR, guild_id, user_id):
    hits = run_file_format(
        CURSOR, "sql/find_user.sql", user_id=user_id, guild_id=guild_id
    )
    if not hits:
        run_file_format(
            CURSOR,
            "sql/add_user.sql",
            user_id=user_id,
            guild_id=guild_id,
            admin_level=0,
        )


def set_admin(CURSOR, guild_id, user_id, admin_level):
    run_file_format(
        CURSOR,
        "sql/set_admin.sql",
        guild_id=guild_id,
        user_id=user_id,
        admin_level=admin_level,
    )


def check_admin(CURSOR, user_id, guild_id, min_admin_level=1):
    hits = run_file_format(
        CURSOR, "sql/find_user.sql", user_id=user_id, guild_id=guild_id
    )
    print(hits)
    admin_level = hits[0][3]
    if admin_level >= min_admin_level:
        return True
    else:
        return False


async def del_messages(CURSOR, bot, guild_id, chore_id):
    messages = run_file_format(CURSOR, "sql/find_message_chore.sql", chore_id=chore_id)
    del_dict = {int(m[1]): int(m[2]) for m in messages}
    for m_id, c_id in del_dict.items():
        channel = bot.get_channel(c_id)
        if channel:
            msg = await channel.fetch_message(m_id)
            await msg.delete()
    run_file_format(CURSOR, "sql/delete_messages.sql", chore_id=chore_id)


async def qmark(message, emoji="❓"):
    await message.add_reaction(emoji)


async def send_chore_message(DATABASE, CURSOR, bot, ctx, guild_id, chore_id):
    chore_data = run_file_format(
        CURSOR, "sql/find_chore.sql", guild_id=guild_id, chore_id=chore_id
    )
    if not chore_data:
        return None
    chore_data = chore_data[0]
    guild_id = chore_data[3]
    user_id = chore_data[1]
    description = chore_data[4]
    assigned_date = chore_data[5]
    member = bot.get_guild(guild_id).get_member(user_id)
    if member is not None:
        username = member.display_name
        url = member.avatar_url
    else:
        username = "Unknown"
        url = ""
    embed = discord.Embed(title=username, description=description)
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
    run_file_format(CURSOR, "sql/add_message.sql", **kwargs)
    DATABASE.commit()
