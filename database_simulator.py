"""
===============================================================================
Title:	Simulator for FreedgeDatabase for the Freedge Tracker System
===============================================================================
Description:	TODO
Authors: 		TODO
Last Edited: 	2-22-2022
Last Edit By:	Madison Werries
"""
import os
import sqlite3
from sqlite3 import Error
from freedge_internal_database.database_constants import *
from caretaker_info_parser import *
from freedge_database import *
def main():
	tdb = load_internal_database(r".\test_data\fdb_needs_updating.db")
	freedges = tdb.get_freedges()
	for f in freedges:
		print(f.freedge_id, " ", f.caretaker_name, " ", f.last_status_update)


if __name__ == '__main__':
	main()
