#!usr/bin/env python3
from utils.initialise import initialise
from utils.teardown import teardown


def run_whole_file(filepath):
    DATABASE, CURSOR = initialise()
    with open(filepath, "r") as f:
        sql = f.read().split(";")
    for command in sql:
        if command != "\n":
            print(f"Executing\n{command}")
            CURSOR.execute(command)
            print("...done")
    DATABASE.commit()
    teardown(CURSOR, DATABASE)


def run_file_format(filepath, **kwargs):
    DATABASE, CURSOR = initialise()
    with open(filepath, "r") as f:
        sql = f.read().format(**kwargs)
    print(f"Executing\n{sql}")
    CURSOR.execute(sql)
    print("...done")
    return_list = [x for x in CURSOR]
    DATABASE.commit()
    teardown(CURSOR, DATABASE)
    return return_list
