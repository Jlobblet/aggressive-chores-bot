USE aggressive_chores_bot;
INSERT INTO chores
(
	user_id
	,guild_id
	,description
	,assigned_date
	,completed_date
)
VALUES
(
	"{user_id}"
	,"{guild_id}"
	,"{description}"
	,TIME_FORMAT("{assigned_date}", "")
	,NULL
);
