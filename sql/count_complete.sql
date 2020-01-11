SELECT COUNT(id) AS complete_chores
FROM chores
WHERE
    guild_id = {guild_id}
    AND user_id = {user_id}
    AND completed_date IS NOT NULL
    AND hidden = 0;
