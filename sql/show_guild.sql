SELECT chore_id
FROM chores
WHERE
	guild_id = {guild_id}
	AND completed_date IS NULL
	AND hidden = 0;
