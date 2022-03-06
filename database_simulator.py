"""
===============================================================================
Title:	Simulator for FreedgeDatabase for the Freedge Tracker System
===============================================================================
Description:	Creates a database using test data that includes freedges
	that are out-of-date, i.e. their last status update was longer than 90
	days ago. Upon running this file,  8 freedge objects are created (these
	objects are automatically set with a default date). 
	
	The program takes these 8 freedge objects and updates their dates to be older
	than 90 days. The 8 default freedge objects and 8 updated freedge objects 
	are printed in the terminal for the user to view. The updated freedge's are 
	loaded into a database titled 'fdb_needs_updating.db' located in the test_data 
	folder.

	To use this test dataset, run the system in the terminal (enter 'python3 
	freedge_tracker.py' in the terminal) and select "Load Database" from the user
	interface. Navigate to the 'fdb_needs_updating.db' database file in the test_data
	folder and and select it. This loads the database data into the system. Now 
	the user can test the system using a complete dataset with both up-to-date and 
	out-of-date freedge entries.


Authors: 	Madison Werries, Ginni Gallagher
Last Edited: 	3-05-2022
Last Edit By:	Ginni Gallagher
"""
from FreedgeDatabase import new_database_from_csv
from datetime import date

def main():
	tdb = new_database_from_csv(r"test_data/fdb_needs_updating.db", "./test_data/freeedge_data_tiny.csv")
	freedges = tdb.get_freedges()
	print("\n Default Freedge objects: \n")
	for i in range(len(freedges)):
		print(freedges[i].freedge_id, " ", freedges[i].caretaker_name, " ",
		freedges[i].last_status_update, " ", freedges[i].permission_to_notify)
	dates = ["2021-10-21", "2022-02-22", "2022-01-19", "2019-06-18", "2021-07-18",
			 "2021-12-12", "2021-12-29", "2022-01-18"]
	for i in range(len(freedges)):
		freedges[i].last_status_update = date.fromisoformat(dates[i])
		tdb.update_freedge(freedges[i])
	
	print("\n\n")
	print("Updated Out-of-Date Freedge objects: \n")
	freedges = tdb.get_freedges()
	for f in freedges:
		print(f.freedge_id, " ", f.caretaker_name, " ", f.last_status_update, " ", f.permission_to_notify)


if __name__ == '__main__':
	main()
