#!usr/bin/env python3
import mysql.connector

from config.SQL import SQL_USER, dbname


def initialise():
    DATABASE = mysql.connector.connect(**SQL_USER)
    CURSOR = DATABASE.cursor(buffered=True, dictionary=True)
    try:
        CURSOR.execute(f"USE {dbname};")
    except mysql.connector.errors.ProgrammingError as e:
        exc = "{}: {}".format(type(e).__name__, e)
        print(
            f"Failed to run\nUSE {dbname};\nDatabase could be missing - ignore if running setup.py. Error:\n{exc}"
        )
    return DATABASE, CURSOR
