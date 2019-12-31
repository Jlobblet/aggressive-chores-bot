#!usr/bin/env python3
import mysql.connector

from config.SQL import SQL_USER
from utils.utils import run_whole_file
from utils.initialise import initialise
from utils.teardown import teardown

DATABASE, CURSOR = initialise()
run_whole_file("sql/setup.sql")
DATABASE.commit()
teardown(CURSOR, DATABASE)
