"""
===============================================================================
Title:	Simulator for freedge_database for the Freedge Tracker System
===============================================================================
Description:	TODO
Authors: 		TODO
Last Edited: 	2-22-2022
Last Edit By:	Madison Werries
"""
from freedge_database import new_database_from_csv
from datetime import date
def main():
	tdb = new_database_from_csv(r"test_data/fdb_needs_updating.db", "./test_data/freeedge_data_tiny.csv")
	freedges = tdb.get_freedges()
	for i in range(len(freedges)):
		print(freedges[i])
	dates = ["2021-10-21", "2022-02-22", "2022-01-19", "2019-06-18", "2021-07-18",
			 "2021-12-12", "2021-12-29", "2022-01-18"]
	for i in range(len(freedges)):
		freedges[i].last_status_update = date.fromisoformat(dates[i])
		tdb.update_freedge(freedges[i])
	
	print("\n\n")
	freedges = tdb.get_freedges()
	for f in freedges:
		print(f.freedge_id, " ", f.caretaker_name, " ", f.last_status_update, " ", f.permission_to_notify)


if __name__ == '__main__':
	main()
