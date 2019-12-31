UPDATE chores
SET hidden = 1
WHERE
    guild_id = {guild_id}
    AND chore_id = {chore_id};
