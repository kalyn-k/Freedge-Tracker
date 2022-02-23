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
from freedge_internal_database.database_constants import *
from caretaker_info_parser import *

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

def new_freedge(conn, freedge_data):
	sql = '''INSERT INTO freedges(freedge_id, project_name,
				network_name, date_installed, contact_lname,
				contact_fname, active_status, last_status_update,
				phone_number, email_address, permission_to_contact,
				preferred_contact_method
				VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'''
	cur = conn.cursor()
	cur.execute(sql, freedge_data)
	conn.commit()
	return cur.lastrowid

def _create_database():
	sql_address_table =\
		"""CREATE TABLE IF NOT EXISTS addresses (
			freedge_id INTEGER PRIMARY KEY,
			street_address varchar(255),
			city varchar(255),
			state_or_province varchar(255),
			zip_code varchar(10),
			country varchar(50)
		);"""
	
	sql_freedges_table =\
		"""CREATE TABLE IF NOT EXISTS freedges (
			freedge_id INTEGER PRIMARY KEY AUTOINCREMENT,
			project_name varchar(255),
			network_name varchar(255),
			date_installed varchar(10),
			contact_last_name varchar(255),
			contact_first_name varchar(255),
			active_status varchar(50),
			last_status_update varchar(10),
			phone_number varchar(50),
			email_address varchar(50),
			permission_to_contact int,
			preferred_contact_method varchar(10)
		);"""
	
	# create a database connection
	conn = create_connection(DATABASE_PATH)
	
	# create tables
	if conn is not None:
		# create projects table
		create_table(conn, sql_address_table)
		
		# create tasks table
		create_table(conn, sql_freedges_table)
	else:
		print("Error! cannot create the database connection.")
		return False
	conn.close()
	return True

def new_database_from_csv():
	success = _create_database()
	if not success:
		print("Error: Could not create the database connection.")
		return False
	# create a database connection
	conn = create_connection(DATABASE_PATH)
	freedge_data = parse_freedge_data_file(DATABASE_CSV)
	conn.close()
	return True


if __name__ == '__main__':
	new_database_from_csv()
