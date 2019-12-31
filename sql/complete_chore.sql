UPDATE chores
SET completed_date = STR_TO_DATE("{completed_date}", "%Y-%m-%d %H:%i:%s")
WHERE
    id = {chore_id};
