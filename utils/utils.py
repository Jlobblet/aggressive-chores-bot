#!usr/bin/env python3
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


async def qmark(message, emoji="❓"):
    await message.add_reaction(emoji)
