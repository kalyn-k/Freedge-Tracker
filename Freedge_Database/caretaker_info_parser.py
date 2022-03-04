"""
===============================================================================
Title:	Caretaker Info Parser for the Freedge Tracker System
===============================================================================
Description:	Read in data from a csv file, input by the user. Parser
				collects data from file rows to determine general data and
				address associated with each freedge. This data is used to populate
				the freedge database from the csv file. 

				Parser works under the assumption that file has been pre-validated
				by a Freedge Administrator and follows a consistent format.
				
Authors: 		Madison Werries, Ginni Gallagher
Last Edited: 	3-2-2022
Last Edit By:	Ginni Gallagher

Edit Log
date		editor		changes
2-22-22		mw			initial doc
2-22-22		mw			created preliminary structure for database
2-23-22		mw			transfered database into new file
3-1-22		gg			documentation
"""

import csv

from Internal_Data.database_constants import *

def remove_whitespace(field_name):
	""" 
	Removes ALL whitespace from a field name. 
	
	Parameters: field_name -> string of data in field

	Return: -> the field_name string stripped of newlines and with no whitespaces
	"""
	return field_name.strip().replace(" ", "")

def _get_headers():
	"""
	Sets headers list using constants defined in database_constants.py

	Parameters: None

	Calls: Called by _parse_row(data_entry); intended for internal use only.

	Returns: headers -> a list of strings to define each column header
	"""
	headers = [
		PROJECT_NAME_KEY,
		NETWORK_NAME_KEY,
		DATE_INSTALLED_KEY,
		CONTACT_NAME_KEY,
		ACTIVE_STATUS_KEY,
		PHONE_NUMBER_KEY,
		EMAIL_ADDRESS_KEY,
		PERMISSION_TO_CONTACT_KEY,
		PREFERRED_METHOD_KEY
	]
	return headers

def _get_address_format():
	"""
	Sets the format of addresses required of the csv file
	using constants defined in database_constants.py

	Parameters: None

	Calls: Called by _parse_address(entry_data); intended for internal use only.

	Returns: headers -> a list of strings to define each address column header
	"""
	headers = [
		STREET_ADDRESS_KEY,
		CITY_KEY,
		STATE_PROVINCE_KEY,
		ZIP_CODE_KEY,
		COUNTRY_KEY
	]
	return headers

def _parse_field(data):
	"""
	Check to ensure data field is not empty.

	Calls: Not called; Madison, is this needed still? (???)
	"""
	if (len(data) == 0):
		return None
	return data

def _parse_address(entry_data):
	"""
	Generates a list containing address data for each freedge.

	Parameters: entry_data -> a row (list of strings) from csv file

	Calls: Called by parse_freedge_data_file(filename) to organize address data

	Returns: parsed -> a list of strings containing the parsed address data fields
	"""
	parsed = []
	headers = _get_address_format()
	for header in headers:
		field = entry_data[header]
		if field is None:
			parsed.append("")
		else:
			parsed.append(entry_data[header])
	return parsed

def _parse_row(entry_data):
	""" 
	Generates a list containing general data for each freedge.

	Parameters: entry_data -> a row (list of strings) from csv file

	Calls: Called by parse_freedge_data_file(filename) to organize genearl freedge data
	
	Returns: parsed -> a list of strings containing the parsed freedge data fields
	"""
	parsed = []
	headers = _get_headers()
	for header in headers:
		field = entry_data[header]
		if field is None:
			parsed.append("")
		else:
			parsed.append(entry_data[header])
	return parsed

def parse_freedge_data_file(filename):
	"""
	Reads in freedge information from a comma-separated csv file. 
	Uses python built-in csv DictReader method to map data from each row
	to a specific fieldname.

	Parameter: filename -> a string defining the name of the csv file to be opened

	Calls:
		Called by:
			freedge_database.compare_databases -> loads a new csv file and compares to 
			state of current database
			freedge_database.new_database_from_csv() -> loads data from csv file into
			database

	Returns: freedge_database_entries -> a list of lists of strings containing all general and 
			address data for each freedge database entry
	
	"""
	freedge_database_entries = []
	
	with open(filename, newline='') as csvfile:
		info_reader = csv.DictReader(csvfile)
		if(info_reader.line_num == 0):
			EOFError("The csv file is empty.")
		for row_data in info_reader:
			general_data = _parse_row(row_data)
			address = _parse_address(row_data)
			freedge_database_entries.append((general_data, address))
		return freedge_database_entries
