#!usr/bin/env python3
import mysql.connector

from config.SQL import SQL_USER
from utils.utils import run_whole_file
from utils.initialise import initialise

DATABASE, CURSOR = initialise()
run_whole_file(CURSOR, "utils/sql/setup.sql")
DATABASE.commit()
DATABASE.close()
