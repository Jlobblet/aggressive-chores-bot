SELECT id
FROM chores
WHERE
	guild_id = {guild_id}
	AND completed_date IS NULL;
