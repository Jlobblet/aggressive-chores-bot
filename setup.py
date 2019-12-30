#!usr/bin/env python3
import mysql.connector

from utils.utils import run_from_file

DATABASE = mysql.connector.connect(host="localhost", user="python", passwd="")
CURSOR = DATABASE.cursor(buffered=True)
run_from_file(CURSOR, "setup.sql")
DATABASE.commit()
DATABASE.close()
