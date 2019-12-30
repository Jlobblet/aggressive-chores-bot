#!usr/bin/env python3
def run_whole_file(CURSOR, filepath):
    with open(filepath, "r") as f:
        sql = f.read().split(";")
    for command in sql:
        if command != "\n":
            print(f"Executing\n{command}")
            CURSOR.execute(command)
            print([x for x in CURSOR])
            print("...done")


def run_file_format(CURSOR, filepath, **kwargs):
    with open(filepath, "r") as f:
        sql = f.read().format(**kwargs)
    print(f"Executing\n{sql}")
    CURSOR.execute(sql)
    print([x for x in CURSOR])
    print("...done")
