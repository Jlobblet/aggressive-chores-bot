#!usr/bin/env python3
from utils.sql_tools import run_file_format


def check_user(guild_id, user_id):
    hits = run_file_format("sql/find_user.sql", user_id=user_id, guild_id=guild_id)
    if not hits:
        run_file_format(
            "sql/add_user.sql", user_id=user_id, guild_id=guild_id,
        )
