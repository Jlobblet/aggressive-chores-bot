INSERT INTO chores
(
    user_id
    ,creator
    ,guild_id
    ,description
    ,assigned_date
    ,completed_date
    ,chore_id
)
VALUES
(
    {user_id}
    ,{creator}
    ,{guild_id}
    ,"{description}"
    ,STR_TO_DATE("{assigned_date}", "%Y-%m-%d %H:%i:%s")
    ,NULL
    ,{chore_id}
);
