#!usr/bin/env python3
def run_from_file(CURSOR, filepath):
    with open(filepath, "r") as f:
        sql = f.read().split(";")
        for command in sql:
            if command != "\n":
                print(f"Executing\n{command}")
                CURSOR.execute(command)
                print([x for x in CURSOR])
                print("...done")
