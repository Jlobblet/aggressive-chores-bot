UPDATE chores
SET
    completed_date = "{completed_date}"
    ,time_taken = "{time_taken}"
WHERE
    guild_id = {guild_id}
    AND chore_id = {chore_id}
    AND completed_date IS NULL
    AND hidden = 0;
