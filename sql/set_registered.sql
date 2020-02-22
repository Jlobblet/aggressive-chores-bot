UPDATE users
SET registered = {registered}
WHERE
    guild_id = {guild_id}
    AND user_id = {user_id}
