"""
===============================================================================
Title:  Freedge Database for the Freedge Tracker System
===============================================================================
Description:    Creates and manages a new SQLite database. This database is loaded
                with data read in from an inputted csv file. This information contains data
                collected by Freedge Administrators via Google Docs regarding location of 
                freedge, name of project, freedge contact information, and more.
                
                The FreedgeDatabase class holds functionality to create an SQLite 
                database connection and implementation for database operations, 
                such as creating a new database, updating a freedge object, returning 
                freedge objects.

Authors:        Madison Werries, Ginni Gallagher, TODO
Last Edited:    3-1-2022
Last Edit By:   Ginni Gallagher 
"""
from os.path import exists
import sqlite3
from sqlite3 import Error
from freedge_internal_database.database_constants import *
from caretaker_info_parser import *
from freedge_data_entry import *

"""
Helpful links used in setting up database connection and database table:

https://www.sqlitetutorial.net/sqlite-python/creating-database/
https://www.sqlitetutorial.net/sqlite-python/create-tables/
"""

class FreedgeDatabase:
	"""
	Holds functionality to create an SQLite database connection, 
	which returns a Connection object that can be used to perform 
	database operations. These operations help create the database,
	update objects within the database, and return database objects
	in readable terms for use by other system components.
	"""
	def __init__(self, db_location):
		"""
		Initializes the location of the SQLite database used by the
		system.
		"""
		self.db_location = db_location
		
	def open_connection(self):
		""" 
		Open and return a database connection defined by db_location.
		Returns: a Connection object - used to perform database operations. 
		"""
		conn = None
		try:
			conn = sqlite3.connect(self.db_location)
			return conn
		except Error as e:
			print(e)
		return conn
	
	def create_table(self, conn, create_table_sql):
		""" 
		Creates a table from the create_table_sql statement.
		A table is an object that contains the data in the database.
		"""
		try:
			c = conn.cursor()
			c.execute(create_table_sql)
		except Error as e:
			print(e)
	
	def new_address(self, conn, address_data, temp=False):
		"""
		TODO
		Description: 

		Inputs:
		Returns:
		"""
		if (temp):
			sql = '''INSERT INTO new_addresses(
						freedge_id, street_address, city,
						state_province, zip_code, country)
					VALUES(?,?,?,?,?,?)'''
		else:
			sql = '''INSERT INTO addresses(
						freedge_id, street_address, city,
						state_province, zip_code, country)
					VALUES(?,?,?,?,?,?)'''
		cur = conn.cursor()
		cur.execute(sql, address_data)
		conn.commit()
		return cur.lastrowid
	
	def new_freedge(self, conn, freedge_data, temp=False):
		"""
		TODO
		Description: 
	
		Inputs:
		Returns:
		"""
		if (temp):
			sql = '''INSERT INTO new_freedges(project_name, network_name, date_installed,
						contact_name, active_status, phone_number, email_address,
						permission_to_contact, preferred_contact_method)
						VALUES(?,?,?,?,?,?,?,?,?)'''
		else:
			sql = '''INSERT INTO freedges(project_name, network_name, date_installed,
						contact_name, active_status, phone_number, email_address,
						permission_to_contact, preferred_contact_method)
						VALUES(?,?,?,?,?,?,?,?,?)'''
		cur = conn.cursor()
		cur.execute(sql, freedge_data)
		conn.commit()
		return cur.lastrowid
	
	def row_to_freedge(self, row):
		""" 
		Converts an SQL row into an instance of the Freedge class. 
        
		TODO
		Inputs: 
			row - List containing strings of data for a specific freedge.
		Returns:
		"""
		# Convert yes/no form responses into the proper Status
		# 		(`Status` class found in freedge_data_entry.py)
		status_string = row[5].upper().strip()
		if (status_string == "YES"):
			status = Status.Active
		elif (status_string == Status.Active.value.upper()):
			status = Status.Active
		elif (status_string == "NO"):
			status = Status.ConfirmedInactive
		elif (status_string == Status.ConfirmedInactive.value.upper()):
			status = Status.ConfirmedInactive
		else:
			status = Status.SuspectedInactive
		# Parse yes/no form responses into booleans
		permission = (row[9].upper().strip() == "YES")
		try:
			installed_date = date.fromisoformat(row[6])
		except:
			installed_date = '0000-00-00'
			
		try:
			last_update = date.fromisoformat(row[4])
		except:
			last_update = '0000-00-00'
			
		# Create a new instance of a FreedgeAddress
		address = FreedgeAddress([row[11], row[12], row[13], row[14], row[15]])
		# Create a new instance of a Freedge:
		new_freedge = Freedge(row[0], row[1], row[2], row[3], address, installed_date, row[10], row[7],
							  row[8], last_update, permission)
		# Set the address and the status of the freedge
		new_freedge.freedge_status = status
		
		return new_freedge
	
	def query_to_freedgelist(self, rows):
		""" 
		Converts all rows in an SQL query to Freedge objects. 
        
		TODO
		Inputs: rows - A list of "rows", each row contains the information
				for a freedge.

		Returns: freedge_list - A list of Freedge objects
		"""
		freedge_list = []
		for row in rows:
			new_freedge = self.row_to_freedge(row)
			freedge_list.append(new_freedge)
		return freedge_list
	
	def get_freedges(self):
		""" 
		Grabs a full list of Freedge Class objects from database. 
		
		Inputs: None
		Returns: A full list of freedges.
		"""
		# Connect to the database
		conn = self.open_connection()
		# Verify that the connection was successful
		if conn is None:
			ConnectionError("Error: Could not connect to the database.")
		
		# Query the database, retrieving all the freedges and their addresses
		cur = conn.cursor()
		cur.execute("SELECT * FROM freedges JOIN addresses USING(freedge_id)")
		# Get the results of the SQL query
		rows = cur.fetchall()
		
		# Parse the SQL query rows into instances of the Freedge class
		# This allows for easier access by the other Freedge Tracker modules
		return self.query_to_freedgelist(rows)
	
	def get_out_of_date(self):
		""" 
		Grabs a list of freedges whose information is out of date. 
		
		Inputs: None
		Returns: A list of freedges that are out of date according to
				their "time_since_last_update" attribute.
		"""
		freedges = self.get_freedges()
		needs_updating = []
		for freedge in freedges:
			t = freedge.time_since_last_update()
			if (t > FIRST_UPDATE_THRESHOLD):
				needs_updating.append(freedge)
		return needs_updating
	
	def update_freedge(self, f):
		""" 
		Update the database data of a specific Freedge. 
		
		TODO
		Inputs:
		Returns:
		"""
		print("updoot")
		conn = self.open_connection()
		# Verify that the connection was successful
		if conn is None:
			ConnectionError("Error: Could not connect to the database.")
		cur = conn.cursor()
		
		# Update the corresponding entry in the freedges table
		sql_update_freedges = '''
			UPDATE freedges
			SET project_name = ?,
				network_name = ?,
				date_installed = ?,
				contact_name = ?,
				active_status = ?,
				last_status_update = ?,
				phone_number = ?,
				email_address = ?,
				permission_to_contact = ?,
				preferred_contact_method = ?
			WHERE freedge_id = ?'''
		
		# Get the proper values to fill in the ? fields
		permission = "no"
		if (f.permission_to_notify):
			permission = "yes"
		
		fields = [f.project_name, f.network_name,
				  f.date_installed.isoformat(), f.caretaker_name,
				  str(f.freedge_status.value), f.last_status_update, f.phone_number,
				  f.email_address, permission,
				  f.preferred_contact_method, str(f.freedge_id)]
		# Execute the update to the table
		cur.execute(sql_update_freedges, fields)

		# Update the corresponding entry in the addresses table
		sql = '''
			UPDATE addresses
			SET street_address = ?,
				city = ?,
				state_province = ?,
				zip_code = ?,
				country = ?
			WHERE freedge_id = ?'''
		
		# FreedgeAddress of the passed-in Freedge f
		addr = f.fridge_location
		# Get the proper values to fill in the ? fields
		fields = [addr.street_address, addr.city, addr.state_province,
				  addr.zip_code, addr.country, str(f.freedge_id)]
		# Execute the update to the table
		cur.execute(sql, fields)
		# Commit the changes and close the connection
		conn.commit()
		conn.close()
		
	def compare_databases(self, new_csv_data):
		""" 
		Returns a tuple (added, removed, modified) of lists of freedges
		whose data is different than the data in the passed csv file argument. 
		
		TODO
		Inputs:
		Returns:
		"""
		
		# Open the connection and verify that it was made successfully
		conn = self.open_connection()
		if conn is None:
			ConnectionError("Failure to connect to the original database.")
		cur = conn.cursor()

		# Define the structure of the new (temporary) addresses table
		sql_new_addresses = \
			""" CREATE TABLE IF NOT EXISTS new_addresses (
				freedge_id INTEGER PRIMARY KEY,
				street_address varchar(255),
				city varchar(255),
				state_province varchar(255),
				zip_code varchar(10),
				country varchar(50)
			);"""
		
		# Define the structure of the new (temporary) freedges table
		sql_new_csv_data = \
			""" CREATE TABLE IF NOT EXISTS new_freedges (
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
		
		# Create the new temporary tables to compare the current data to
		cur.execute("DROP TABLE IF EXISTS new_addresses;")
		cur.execute("DROP TABLE IF EXISTS new_freedges;")
		self.create_table(conn, sql_new_csv_data)
		self.create_table(conn, sql_new_addresses)
		
		# Parse the data from the new csv file
		new_freedge_dataset = parse_freedge_data_file(new_csv_data)
		# Insert the data into the new temporary tables
		for freedge_data in new_freedge_dataset:
			fid = self.new_freedge(conn, freedge_data[0], True)
			address_data = [str(fid)] + freedge_data[1]
			self.new_address(conn, address_data, True)
		
		# =====================================================================
		# Get the freedges that would be ADDED to the database
		# =====================================================================
		sql = '''SELECT new.freedge_id, new.project_name, new.network_name, new.contact_name,
		 				new.date_installed, new.active_status, new.last_status_update,
		 				new.phone_number, new.email_address, new.permission_to_contact,
		 				new.preferred_contact_method, new.street_address, new.city,
		 				new.state_province, new.zip_code, new.country  FROM (new_freedges f2
					JOIN new_addresses a2
					USING (freedge_id))
					AS new
				WHERE NOT EXISTS(
					SELECT * FROM (freedges f1
					JOIN addresses a1
					USING(freedge_id))
					AS old
				WHERE old.project_name = new.project_name)
				'''
		cur.execute(sql)
		rows_to_add = cur.fetchall()
		
		# =====================================================================
		# Get the freedges that would be REMOVED from the database
		# =====================================================================
		sql = '''SELECT old.freedge_id, old.project_name, old.network_name, old.contact_name,
		 				old.date_installed, old.active_status, old.last_status_update,
		 				old.phone_number, old.email_address, old.permission_to_contact,
		 				old.preferred_contact_method, old.street_address, old.city,
		 				old.state_province, old.zip_code, old.country FROM (freedges f1
					JOIN addresses a1
					USING(freedge_id))
					AS old
				WHERE NOT EXISTS(
					SELECT * FROM (new_freedges f2
					JOIN new_addresses a2
					USING (freedge_id))
					AS new
				WHERE old.project_name = new.project_name)
				'''
		cur.execute(sql)
		rows_to_remove = cur.fetchall()
		
		# =====================================================================
		# Get the freedges that would be CHANGED within the database
		# =====================================================================
		sql = '''SELECT old.freedge_id, old.project_name, old.network_name, old.contact_name,
		 				old.date_installed, old.active_status, old.last_status_update,
		 				old.phone_number, old.email_address, old.permission_to_contact,
		 				old.preferred_contact_method, old.street_address, old.city,
		 				old.state_province, old.zip_code, old.country FROM (freedges f1
					JOIN addresses a1
					USING(freedge_id))
					AS old
				WHERE EXISTS(
					SELECT * FROM (new_freedges f2
					JOIN new_addresses a2
					USING (freedge_id))
					AS new
				WHERE old.project_name = new.project_name
					AND (old.network_name != new.network_name
					OR old.contact_name != new.contact_name
					OR old.date_installed != new.date_installed
					OR old.active_status != new.active_status
					OR old.last_status_update != new.last_status_update
					OR old.phone_number != new.phone_number
					OR old.email_address != new.email_address
					OR old.permission_to_contact != new.permission_to_contact
					OR old.preferred_contact_method != new.preferred_contact_method
					OR old.street_address != new.street_address
					OR old.city != new.city
					OR old.state_province != new.state_province
					OR old.zip_code != new.zip_code
					OR old.country != new.country))
				'''
		cur.execute(sql)
		rows_modify_from = cur.fetchall()
		
		sql = '''SELECT old.freedge_id, old.project_name, old.network_name, old.contact_name,
		 				old.date_installed, old.active_status, old.last_status_update,
		 				old.phone_number, old.email_address, old.permission_to_contact,
		 				old.preferred_contact_method, old.street_address, old.city,
		 				old.state_province, old.zip_code, old.country  FROM (freedges f1
							JOIN addresses a1
							USING(freedge_id))
							AS old
						WHERE EXISTS(
							SELECT * FROM (new_freedges f2
							JOIN new_addresses a2
							USING (freedge_id))
							AS new
						WHERE old.project_name = new.project_name
							AND (old.network_name != new.network_name
							OR old.contact_name != new.contact_name
							OR old.date_installed != new.date_installed
							OR old.active_status != new.active_status
							OR old.last_status_update != new.last_status_update
							OR old.phone_number != new.phone_number
							OR old.email_address != new.email_address
							OR old.permission_to_contact != new.permission_to_contact
							OR old.preferred_contact_method != new.preferred_contact_method
							OR old.street_address != new.street_address
							OR old.city != new.city
							OR old.state_province != new.state_province
							OR old.zip_code != new.zip_code
							OR old.country != new.country))
						'''
		cur.execute(sql)
		rows_modify_to = cur.fetchall()

		to_add = self.query_to_freedgelist(rows_to_add)
		to_remove = self.query_to_freedgelist(rows_to_remove)
		to_modify = []
		for i in range(len(rows_modify_from)):
			f1 = self.row_to_freedge(rows_modify_from[i])
			f2 = self.row_to_freedge(rows_modify_to[i])
			to_modify.append((f1, f2))
		
		cur.execute("DROP TABLE IF EXISTS new_addresses;")
		cur.execute("DROP TABLE IF EXISTS new_freedges;")
		
		# Close the connection
		conn.close()
		return (to_add, to_remove, to_modify)

def exists_internal_database(db_path):
	""" 
	Returns whether or not there exists a database at the given path. 
	
	TODO
	Inputs:
	Returns:
	"""
	return(exists(db_path))

def load_internal_database(db_path):
	""" 
	Loads and returns the database at the given path. 
	
	TODO
	Inputs:
	Returns:
	"""
	try:
		sqlite3.connect(DATABASE_PATH)
	except Error as e:
		ConnectionError(e, " Unable to find or connect to database at the given path.")
		return None
	freedgeDB = FreedgeDatabase(db_path)
	return freedgeDB
	
def new_database_from_csv(db_path, csv_file_path):
	""" 
	Creates and returns a new internal database from a csv file. 
	
	TODO
	Inputs:
	Returns:
	"""

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
			contact_name varchar(255),
			date_installed date,
			active_status varchar(50) DEFAULT 'active',
			last_status_update date DEFAULT (DATE('now')),
			phone_number varchar(50),
			email_address varchar(50),
			permission_to_contact int,
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
		freedgeDB.create_table(conn, sql_address_table)
		
		# create tasks table
		sql = "DROP TABLE IF EXISTS freedges;"
		cur.execute(sql)
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
	new_csv = r".\test_data\freeedge_data_tiny_edited.csv"
	fdb = new_database_from_csv(DATABASE_PATH, DATABASE_CSV)
	fs = fdb.get_freedges()
	fs[0].freedge_status = Status.SuspectedInactive
	fdb.update_freedge(fs[0])
	(add, remove, modidfy) = fdb.compare_databases(new_csv)
	
	#fdb = load_internal_database(DATABASE_PATH)
