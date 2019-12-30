DELETE FROM chores
WHERE
    id = {chore_id}
    AND guild_id = {guild_id};
