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
from freedge_data_entry import *

# https://www.sqlitetutorial.net/sqlite-python/creating-database/
# https://www.sqlitetutorial.net/sqlite-python/create-tables/

class FreedgeDatabase:
	def __init__(self, db_location):
		self.db_location = db_location
		
	def open_connection(self):
		""" Opens and returns this database's connection.
			:returns the Connection variable. """
		conn = None
		try:
			conn = sqlite3.connect(self.db_location)
			return conn
		except Error as e:
			print(e)
		return conn
	
	def create_table(self, conn, create_table_sql):
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
	
	def new_address(self, conn, address_data):
		sql = '''INSERT INTO addresses(
					freedge_id, street_address, city,
					state_province, zip_code, country
					)
					VALUES(?,?,?,?,?,?)'''
		cur = conn.cursor()
		cur.execute(sql, address_data)
		conn.commit()
		return cur.lastrowid
	
	def new_freedge(self, conn, freedge_data):
		sql = '''INSERT INTO freedges(project_name, network_name, date_installed,
					contact_name, active_status, phone_number, email_address,
					permission_to_contact, preferred_contact_method)
					VALUES(?,?,?,?,?,?,?,?,?)'''
		cur = conn.cursor()
		cur.execute(sql, freedge_data)
		conn.commit()
		return cur.lastrowid
	
	def get_freedges(self):
		""" Returns a full list of Freedge Class objects. """
		conn = self.open_connection()
		if conn is None:
			ConnectionError("Error: Could not create the database connection.")
		cur = conn.cursor()
		cur.execute("SELECT freedge_id, project_name, network_name, contact_name, "
					"active_status, last_status_update, phone_number, "
					"email_address, permission_to_contact, "
					"preferred_contact_method, street_address, city, "
					"state_province, zip_code, country, date_installed "
					"FROM freedges JOIN addresses USING(freedge_id)")
		rows = cur.fetchall()
		freedge_list = []
		for row in rows:
			freedge_address = FreedgeAddress(row[10], row[11], row[12], row[13], row[14])
			freedge_obj = Freedge(row[0], row[1], row[2], row[3], freedge_address, row[9], row[6], row[7], row[15])
			freedge_list.append(freedge_obj)
		return freedge_list
	
	#def get_out_of_date(self):
	
	# def compare_databases()
	# def update_database_from_csv()

def exists_internal_database(db_path):
	""" Returns whether or not there exists a database at the given path. """
	try:
		sqlite3.connect(db_path)
	except Error:
		return False
	return True

def load_internal_database(db_path):
	""" Loads and returns the database at the given path. """
	try:
		sqlite3.connect(DATABASE_PATH)
	except Error as e:
		ConnectionError(e, " Unable to find or connect to database at the given path.")
		return None
	freedgeDB = FreedgeDatabase(db_path)
	return freedgeDB
	
def new_database_from_csv(db_path, csv_file_path):
	""" Creates and returns a new internal database from a csv file. """

	# This defines the structure of the addresses table
	sql_address_table = \
		""" CREATE TABLE IF NOT EXISTS addresses (
			freedge_id INTEGER PRIMARY KEY,
			street_address varchar(255),
			city varchar(255),
			state_province varchar(255),
			zip_code varchar(10),
			country varchar(50)
		);"""
	
	# This defines the structure of the freedges table
	sql_freedges_table = \
		""" CREATE TABLE IF NOT EXISTS freedges (
			freedge_id INTEGER PRIMARY KEY AUTOINCREMENT,
			project_name varchar(255),
			network_name varchar(255),
			date_installed date,
			contact_name varchar(255),
			active_status varchar(50),
			last_status_update date DEFAULT NULL,
			phone_number varchar(50),
			email_address varchar(50),
			permission_to_contact int DEFAULT 0,
			preferred_contact_method varchar(10)
		);"""
	# Create the new FreedgeDatabase class object
	freedgeDB = FreedgeDatabase(db_path)
	
	# create a database connection
	conn = freedgeDB.open_connection()
	
	# If the connection was successful, create the tables
	if conn is not None:
		cur = conn.cursor()
		
		# create projects table
		sql = "DROP TABLE IF EXISTS addresses;"
		cur.execute(sql)
		conn.commit()
		freedgeDB.create_table(conn, sql_address_table)
		
		# create tasks table
		sql = "DROP TABLE IF EXISTS freedges;"
		cur.execute(sql)
		conn.commit()
		freedgeDB.create_table(conn, sql_freedges_table)
	else:
		ConnectionError("Error: Could not create the database connection.")
	
	# Now that the (empty) tables have been created, parse data from the csv file
	freedge_dataset = parse_freedge_data_file(csv_file_path)
	# Insert all the parsed data into the database tables
	for freedge_data in freedge_dataset:
		# Add the individual freedge to the SQL table
		fid = freedgeDB.new_freedge(conn, freedge_data[0])
		address_data = [str(fid)] + freedge_data[1]
		freedgeDB.new_address(conn, address_data)
	
	# Commit the changes
	conn.commit()
	# Close the connection
	conn.close()
	# Return the FreedgeDatabase class instance
	return freedgeDB


if __name__ == '__main__':
	fdb = new_database_from_csv(DATABASE_PATH, DATABASE_CSV)
	#fdb = load_internal_database(DATABASE_PATH)
	freedges = fdb.get_freedges()
	for f in freedges:
		print(f)
