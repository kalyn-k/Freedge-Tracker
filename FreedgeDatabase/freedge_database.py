"""
===============================================================================
Title:  Freedge Database for the Freedge Tracker System
===============================================================================
Description:    Creates and manages a new SQLite database. This database is loaded
                with data read in from an input csv file. This information contains data
                collected by Freedge Administrators via Google Forms regarding location of 
                freedge, name of project, freedge contact information, and more.

				This file manages SQL executions using python programming. The organization 
				and abstraction provides ease of reading for programmers not familiar with
				SQL databases.

Authors:        Madison Werries, Ginni Gallagher
Last Edited:    3-6-2022
Last Edit By:   Madison Werries
"""
from os.path import exists
import sqlite3
from sqlite3 import Error
from InternalData.freedge_constants import *
from datetime import date
import FreedgeDatabase as FD
from FreedgeDatabase.freedge_data_entry import Status

"""
Helpful links used in setting up database connection and database table:

https://www.sqlitetutorial.net/sqlite-python/creating-database/
https://www.sqlitetutorial.net/sqlite-python/create-tables/
"""

class FreedgeDatabase:
	"""
	Holds functionality to create an SQLite database connection, which returns
	an SQLite Connection that can be used to perform database operations.
	These operations help create the database, update entries within the
	database, and convert entries in the database into Freedge objects so that
	they are more easily parsable by other modules in the system.
	"""
	def __init__(self, db_location):
		"""
		Initializes the location of the SQLite database used by the
		system.

		Parameters: db_location -> string defining location of file.

		Returns: None
		"""
		self.db_location = db_location
		
	def open_connection(self):
		""" 
		Open and return a database connection defined by db_location.

		Parameters: None

		Returns: 
			An SQLite Connection object -> used to perform database operations.
		"""
		conn = None
		try:
			conn = sqlite3.connect(self.db_location)
			return conn
		except Error as e:
			Error(e, "Failed to connect to the database at: ", self.db_location)
		return conn
	
	def create_table(self, conn, create_table_sql):
		""" 
		Creates an SQL table in the databse using the create_table_sql statement.

		Parameters:
			conn -> An open Connection object linked to the database.

		Returns: None
		"""
		try:
			c = conn.cursor()
			c.execute(create_table_sql)
		except Error as e:
			Error(e, "Failed to connect to the database at: ", self.db_location)

	def new_address(self, conn, address_data, temp=False):
		"""
		Inserts a new address into the SQLite database's 'addresses' table.

		Parameters:
			conn -> An open Connection object linked to the database.
			address_data -> An array containing the address data of specific
							freedge. These values will be fed into the
							SQLite INSERT statement.
			temp -> A boolean used to determine whether to store the new
					address in the permanent table, or the temporary one
					called 'new_addresses,' which is only used for database
					comparison. Default value is False.

		Returns: An int, which is the database ID of the created address.
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
		Inserts a new freedge into the SQLite database's 'freedges' table.
	
		Parameters:
			conn -> An open Connection object linked to the database.
			freedge_data -> An array containing the address data of specific
							freedge. These values will be fed into the
							SQLite INSERT statement.
			temp -> A boolean used to determine whether to store the new
					freedge in the permanent table, or the temporary one
					called 'new_freedges,' which is only used for database
					comparison. Default is False.

		Returns: An int, which is the database ID of the new freedge entry.
		"""
		if (temp):
			sql = '''INSERT INTO new_freedges(project_name, network_name, date_installed,
						contact_name, active_status, phone_number, email_address,
						permission_to_contact, preferred_contact_method,
						last_status_update)
						VALUES(?,?,?,?,?,?,?,?,?,?)'''
		else:
			sql = '''INSERT INTO freedges(project_name, network_name, date_installed,
						contact_name, active_status, phone_number, email_address,
						permission_to_contact, preferred_contact_method,
						last_status_update)
						VALUES(?,?,?,?,?,?,?,?,?,?)'''
		cur = conn.cursor()
		cur.execute(sql, freedge_data)
		conn.commit()
		return cur.lastrowid
	
	def row_to_freedge(self, row):
		""" 
		Converts an SQL row into an instance of the Freedge class. 
        
		Parameters: row -> List of strings containing data for a freedge. 

		Returns: new_freedge -> A instance of the Freedge class.
		"""
		# Convert yes/no form responses into the proper Status
		# 		(`Status` class found in freedge_data_entry.py)
		active_str = Status.Active.value.upper()
		sus_inact_str = Status.SuspectedInactive.value.upper()
		conf_inact_str = Status.ConfirmedInactive.value.upper()
		unknown_str = Status.Unknown.value.upper()
		
		status_str = row[5].upper().strip()
		# Read in the status of the user from the given row value, accepting
		# a few potential formats
		if (status_str == "YES" or status_str == active_str):
			status = Status.Active
		elif (status_str == "NO" or status_str == conf_inact_str):
			status = Status.ConfirmedInactive
		elif (status_str == sus_inact_str):
			status = Status.SuspectedInactive
		else:
			status = Status.Unknown
		
		# Parse yes/no form responses into booleans
		permission = (row[9].upper().strip() == "YES")
		try:
			installed_date = date.fromisoformat(row[6])
		except:
			installed_date = '-'
		try:
			last_update = date.fromisoformat(row[4])
		except:
			last_update = '-'
			
		# Create a new instance of a FreedgeAddress
		address = FD.FreedgeAddress([row[11], row[12], row[13], row[14], row[15]])
		# Create a new instance of a Freedge:
		new_freedge = FD.Freedge(row[0], row[1], row[2], row[3], address, installed_date, row[10], row[7],
							  row[8], last_update, permission)
		# Set the address and the status of the freedge
		new_freedge.freedge_status = status
		
		return new_freedge
	
	def query_to_freedgelist(self, rows):
		""" 
		Converts all the rows in an SQL query into a list of Freedge objects.
        
		Parameters: rows -> A list of entries resulting from an SQLite query,
							each row containing data which can be used to
							build an object of type Freedge.

		Returns: freedge_list -> A list of Freedge objects.
		"""
		freedge_list = []
		for row in rows:
			new_freedge = self.row_to_freedge(row)
			freedge_list.append(new_freedge)
		return freedge_list
	
	def get_freedges(self):
		""" 
		Retrieves a list of all of the entries in the database in the form of Freedge objects.
		Parameters: None

		Returns: A list of Freedge objects.
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
		
		Parameters: None

		Returns: 
			A list of Freedge objects corresponding to the entries in the
			database whose statuses are out of date.
		"""
		freedges = self.get_freedges()
		needs_updating = []
		for freedge in freedges:
			t = freedge.time_since_last_update()
			if (t is not None):
				if (t > FIRST_UPDATE_THRESHOLD):
					needs_updating.append(freedge)
		return needs_updating
	
	def update_freedge(self, f):
		""" 
		Update the database to reflect the information contained in a specific
		Freedge object, located by freedge_id.
		
		Parameters: f -> the Freedge object whose data needs to be updated
						 within the database.

		Returns: None
		"""
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
				  f.date_installed, f.caretaker_name,
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
		Determines what freedges have data that is different from the data in
		the passed csv file argument. This may be used in the future to display
		information to the user about data which will be overridden if they
		want to upload an updated version of a database that they have loaded
		in before.
		
		Parameters: new_csv_data -> a string of the name of the desired csv file

		Returns:
			Tuple of lists of freedges whose data is different from the 
			data in the passed in csv file argument -> (to_add, to_remove, to_modify).
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
		new_freedge_dataset = FD.parse_freedge_data_file(new_csv_data)
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
	
	Parameters: db_path -> a string defining the path to be tested.
	
	Returns: exists(db_path) -> a bool True or False if database exists
	"""
	return(exists(db_path))

def load_internal_database(db_path):
	""" 
	Loads and returns the database at the given path. 
	
	Parameters: db_path -> a string indicating the path of the database to be loaded.

	Returns:
		freedgeDB -> Instance of FreedgeDatabase object.
	"""
	try:
		sqlite3.connect(DATABASE_PATH_INFO)
	except Error as e:
		ConnectionError(e, " Unable to find or connect to database at the given path.")
		return None
	freedgeDB = FreedgeDatabase(db_path)
	return freedgeDB
	
def new_database_from_csv(db_path: str, csv_file_path: str):
	""" 
	Creates and returns a new internal database from a csv file. 
	
	Parameters:
		db_path -> str Path of database to be created.
		csv_file_path -> str Path of the input csv file.

	Returns:
		freedgeDB - a FreedgeDatabase class instance.
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
			active_status varchar(50) DEFAULT 'Unknown',
			last_status_update date DEFAULT NULL,
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
	freedge_dataset = FD.parse_freedge_data_file(csv_file_path)
	# Insert all the parsed data into the database tables
	for freedge_data in freedge_dataset:
		# Add the individual freedge to the SQL table
		# So long as there is SOME kind of response to their preferred contact method,
		# set the most recent update to today.
		data_fields = freedge_data[0]
		fid = freedgeDB.new_freedge(conn, data_fields)
		address_data = [str(fid)] + freedge_data[1]
		freedgeDB.new_address(conn, address_data)
	
	# Commit the changes
	conn.commit()
	# Close the connection
	conn.close()
	# Return the FreedgeDatabase class instance
	return freedgeDB
