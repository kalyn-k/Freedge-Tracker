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
from freedge_internal_database import database_constants as dbconst

def _parse_field(data):
	if (len(data) == 0):
		return None
	return data

def _parse_row(entry_data):
	""" Parses the freedge information in an array of strings. """
	data_array = []
	for entry in entry_data:
		data_array.append(_parse_field(entry))
	return data_array
	
def parse_freedge_data_file(filename):
	""" Reads in freedge information from a comma-separated csv file. """
	freedge_database_entries = []
	
	with open(filename, newline='') as csvfile:
		info_reader = csv.DictReader(csvfile)
		if(info_reader.line_num == 0):
			EOFError("The csv file is empty.")
		for freedge_data in info_reader:
			freedge_database_entries.append(freedge_data)
			print(freedge_data)
