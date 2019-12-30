#!usr/bin/env python3
import datetime
from utils.utils import run_file_format


def add_chore(CURSOR, user_id, guild_id, description):
    kwargs = {
        "user_id": user_id,
        guild_id: "guild_id",
        "description": description,
        "assigned_date": datetime.datetime.now().strftime("%Y-%m-%d (%a) %H:%M:%S"),
    }
    run_file_format(CURSOR, "utils/sql/add_chore.sql", **kwargs)
