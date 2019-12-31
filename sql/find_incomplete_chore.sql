SELECT *
FROM chores
WHERE
    id = {chore_id}
    AND completed_date IS NULL
    AND hidden = 0;
