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
	# Creates a database in a file on disk, returns the connection to it
	def __init__(self, db_location):
		self.db_location = db_location
		sql_address_table = \
			""" CREATE TABLE IF NOT EXISTS addresses (
				freedge_id INTEGER PRIMARY KEY,
				street_address varchar(255),
				city varchar(255),
				state_province varchar(255),
				zip_code varchar(10),
				country varchar(50)
			);"""
		
		sql_freedges_table = \
			""" CREATE TABLE IF NOT EXISTS freedges (
				freedge_id INTEGER PRIMARY KEY AUTOINCREMENT,
				project_name varchar(255),
				network_name varchar(255),
				date_installed varchar(10),
				contact_name varchar(255),
				active_status varchar(50),
				last_status_update varchar(10) DEFAULT 'dd-mm-yyyy',
				phone_number varchar(50),
				email_address varchar(50),
				permission_to_contact int,
				preferred_contact_method varchar(10)
			);"""
		
		# create a database connection
		conn = self.open_connection()
		
		# create tables
		if conn is not None:
			cur = conn.cursor()
			sql = "DROP TABLE IF EXISTS addresses;"
			cur.execute(sql)
			conn.commit()
			# create projects table
			self.create_table(conn, sql_address_table)
			
			sql = "DROP TABLE IF EXISTS freedges;"
			cur.execute(sql)
			conn.commit()
			# create tasks table
			self.create_table(conn, sql_freedges_table)
		else:
			ConnectionError("Error: Could not create the database connection.")
		conn.close()
		
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
		freedges = []
		for row in rows:
			freedge_address = FreedgeAddress(row[10], row[11], row[12], row[13], row[14])
			freedge_obj = Freedge(row[0], row[1], row[2], row[3], freedge_address, row[9], row[6], row[7], row[15])
			freedges.append(freedge_obj)
		return freedges
		
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
	freedgeDB = FreedgeDatabase(db_path)
	# Create the database in the location specified by DATABASE_PATH
	# open the created database connection
	conn = freedgeDB.open_connection()
	freedge_dataset = parse_freedge_data_file(csv_file_path)
	
	for freedge_data in freedge_dataset:
		# Add the individual freedge to the SQL table
		fid = freedgeDB.new_freedge(conn, freedge_data[0])
		address_data = [str(fid)] + freedge_data[1]
		freedgeDB.new_address(conn, address_data)
	
	# Close the connection
	conn.close()
	return freedgeDB


if __name__ == '__main__':
	fdb = new_database_from_csv(DATABASE_PATH, DATABASE_CSV)
	fdb.get_freedges()
