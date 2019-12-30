#!usr/bin/env python3
import mysql.connector

from config.SQL import SQL_USER
from utils.utils import run_from_file

DATABASE = mysql.connector.connect(**SQL_USER)
CURSOR = DATABASE.cursor(buffered=True)
run_from_file(CURSOR, "utils/sql/setup.sql")
DATABASE.commit()
DATABASE.close()
