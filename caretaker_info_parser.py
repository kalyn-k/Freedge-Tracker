"""
===============================================================================
Title:	Caretaker Info Parser for the Freedge Tracker System
===============================================================================
Description:	Reads in data from a CSV file, formatting as needed for the
				Freedge Database module.
				
Authors: 		TODO
Last Edited: 	2-22-2022
Last Edit By:	Madison Werries
"""

import csv
import string

from freedge_internal_database.database_constants import *

def remove_whitespace(field_name):
	""" Removes ALL whitespace from a field name. """
	return field_name.strip().replace(" ", "")

def _get_headers():
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
	headers = [
		STREET_ADDRESS_KEY,
		CITY_KEY,
		STATE_PROVINCE_KEY,
		ZIP_CODE_KEY,
		COUNTRY_KEY
	]
	return headers

def _parse_field(data):
	if (len(data) == 0):
		return None
	return data

def _parse_address(entry_data):
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
	""" Parses the freedge information in an array of strings. """
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
	""" Reads in freedge information from a comma-separated csv file. """
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
