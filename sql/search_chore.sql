SELECT chore_id
FROM chores
WHERE
    user_id = {user_id}
    AND creator = {creator}
    AND guild_id = {guild_id}
    AND description = "{description}"
    AND assigned_date = STR_TO_DATE("{assigned_date}", "%Y-%m-%d %H:%i:%s")
    AND hidden = 0;
