#!usr/bin/env python3
import mysql.connector

from config.SQL import SQL_USER



def initialise():
    DATABASE = mysql.connector.connect(**SQL_USER)
    CURSOR = DATABASE.cursor()
    try:
        CURSOR.execute("USE aggressive_chores_bot;")
    except:
        pass
    return DATABASE, CURSOR
