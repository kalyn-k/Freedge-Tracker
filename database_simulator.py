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
	tdb = new_database_from_csv(r".\test_data\fdb_needs_updating.db", DATABASE_CSV)
	freedges = tdb.get_freedges()
	for f in freedges:
		print(f.freedge_id, " ", f.caretaker_name, " ", f.last_status_update)
	date1 = "2021-10-21"
	date2 = "2019-06-18"
	date3 = "2021-07-18"
	freedges[0].last_status_update = date.fromisoformat(date1)
	freedges[4].last_status_update = date.fromisoformat(date2)
	freedges[5].last_status_update = date.fromisoformat(date3)
	tdb.update_freedge(freedges[0])
	tdb.update_freedge(freedges[4])
	tdb.update_freedge(freedges[5])
	print("\n\n")
	freedges = tdb.get_freedges()
	for f in freedges:
		print(f.freedge_id, " ", f.caretaker_name, " ", f.last_status_update)


if __name__ == '__main__':
	main()
