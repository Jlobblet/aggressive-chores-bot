#!usr/bin/env pythoin3
import discord


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


def check_user(CURSOR, message):
    user_id = message.author.id
    guild_id = message.guild.id
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


async def del_messages(CURSOR, bot, chore_id):
    messages = run_file_format(CURSOR, "sql/find_message_chore.sql", chore_id=chore_id)
    del_dict = {int(m[2]): int(m[1]) for m in messages}
    for c_id, m_id in del_dict.items():
        channel = bot.get_channel(c_id)
        if channel:
            msg = await channel.fetch_message(m_id)
            await msg.delete()
    run_file_format(CURSOR, "sql/delete_messages.sql", chore_id=chore_id)


async def qmark(message, emoji="❓"):
    await message.add_reaction(emoji)
