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

def parse_freedge_data(entry_data):
	""" Parses the freedge information in an array of strings. """
	project_name = entry_data[0]
	network_name = entry_data[1]
	street_address = entry_data[2]
	city = entry_data[3]
	state_or_province = entry_data[4]
	zip_code = entry_data[5]
	country = entry_data[6]
	main_contact = entry_data[7]
	loc_type = entry_data[11] # Row L
	date_installed = entry_data[12]
	status = entry_data[19]


def parse_freedgedata(filename: csv):
	""" Reads in freedge information from a comma-separated csv file. """
	with open(filename, newline='') as csvfile:
		info_reader = csv.reader(csvfile)
		for freedge_data in info_reader:
			print("")
		