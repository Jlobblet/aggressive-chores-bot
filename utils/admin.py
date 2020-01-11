#!usr/bin/env python3
from utils.user import check_user
from utils.sql_tools import run_file_format


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
