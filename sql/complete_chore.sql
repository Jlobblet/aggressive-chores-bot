UPDATE chores
SET completed_date = STR_TO_DATE("{completed_date}", "%Y-%m-%d %H:%i:%s")
WHERE
    guild_id = {guild_id}
    AND chore_id = {chore_id}
    AND completed_date IS NULL
    AND hidden = 0;
