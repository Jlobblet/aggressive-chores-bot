SELECT MAX(chore_id) as max_chore_id
FROM chores
WHERE guild_id = {guild_id};
