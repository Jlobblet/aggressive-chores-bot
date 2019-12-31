INSERT INTO messages
(
    message_id
    ,channel_id
    ,chore_id
    ,creation_time
)
VALUES
(
    {message_id}
    ,{channel_id}
    ,{chore_id}
    ,STR_TO_DATE("{creation_time}", "%Y-%m-%d %H:%i:%s")
);
