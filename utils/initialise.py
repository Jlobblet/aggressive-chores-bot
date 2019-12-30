#!usr/bin/env python3
import mysql.connector

from config.SQL import SQL_USER, dbname


def initialise():
    DATABASE = mysql.connector.connect(**SQL_USER)
    CURSOR = DATABASE.cursor()
    CURSOR.execute(f"USE {dbname};")
    return DATABASE, CURSOR
