SELECT *
FROM messages
WHERE
    message_id = {message_id}
    AND channel_id = {channel_id};
