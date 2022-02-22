"""
===============================================================================
Title:	Freedge Database for the Freedge Tracker System
===============================================================================
Description:	TODO
Authors: 		TODO
Last Edited: 	2-22-2022
Last Edit By:	Madison Werries
"""

import sqlite3
from sqlite3 import Error
import sys

# https://www.sqlitetutorial.net/sqlite-python/creating-database/
# https://www.sqlitetutorial.net/sqlite-python/create-tables/

# Creates a database in a file on disk, returns the connection to it
def create_connection(db_file):
	""" create a database connection to the SQLite database
		specified by db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	
	return conn

def create_table(conn, create_table_sql):
	""" create a table from the create_table_sql statement
	:param conn: Connection object
	:param create_table_sql: a CREATE TABLE statement
	:return:
	"""
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)

def create_database():
	# TODO: change location of the database
	database = r"C:\sqlite\db\pythonsqlite.db"
	
	sql_create_projects_table =\
		"""CREATE TABLE IF NOT EXISTS projects (
			id integer PRIMARY KEY,
			name text NOT NULL,
			begin_date text,
			end_date text
		);"""

	sql_create_tasks_table =\
		"""CREATE TABLE IF NOT EXISTS tasks (
			id integer PRIMARY KEY,
			name text NOT NULL,
			priority integer,
			status_id integer NOT NULL,
			project_id integer NOT NULL,
			begin_date text NOT NULL,
			end_date text NOT NULL,
			FOREIGN KEY (project_id) REFERENCES projects (id)
		);"""
	
	# create a database connection
	conn = create_connection(database)
	
	# create tables
	if conn is not None:
		# create projects table
		create_table(conn, sql_create_projects_table)
		
		# create tasks table
		create_table(conn, sql_create_tasks_table)
	else:
		print("Error! cannot create the database connection.")
	
if __name__ == '__main__':
	create_database()
