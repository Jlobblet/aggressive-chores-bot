UPDATE users
SET admin_level = {admin_level}
WHERE
    guild_id = {guild_id}
    AND user_id = {user_id}
