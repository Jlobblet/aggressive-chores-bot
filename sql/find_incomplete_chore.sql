SELECT *
FROM chores
WHERE
    guild_id = {guild_id}
    AND chore_id = {chore_id}
    AND completed_date IS NULL
    AND hidden = 0;
