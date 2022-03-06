"""
===============================================================================
Title:	Simulator for FreedgeDatabase for the Freedge Tracker System
===============================================================================
Description:	This script is for testing purposes only.

				The database simulator is used to create an imaginary database
				which includes freedges whose statuses are out-of-date (i.e.
				their last status update was longer than the number of days
				specified at FIRST_UPDATE_THRESHOLD in the constants file,
				freedge_constants.py.
				
===============================================================================
Instructions: How To Utilize this test script:
===============================================================================
(1)	Upon running this file, a database is first created from a csv file
	containing test data which is formatted in the way that the Freedge
	organization currently formats their data in CSV files.
	
(2)	The program then updates the created database, manually setting some of
	their last_status_update dates to be older than the out-of-date threshold.
	The new values are printed to the terminal to allow for the verification of
	the new dates.
	
(3)	The test database which is created is titled 'fdb_needs_updating.db',
	located in the test_data folder.

(4) To use this test dataset, run the system in the terminal (enter 'python3
	freedge_tracker.py' in the terminal) and select "Load Database" from the
	user interface. Navigate to the 'fdb_needs_updating.db' database file in
	the test_data folder and and select it. This loads the database data into
	the system. Now the user can test the system using a complete dataset with
	both up-to-date and out-of-date freedge entries.
	
Note:	more information can be found in the 'Testing' appendix of the
	 	Programmer_Documentation.pdf file.
===============================================================================
Authors: 	Madison Werries, Ginni Gallagher
Last Edited: 	3-06-2022
Last Edit By:	Madison Werries
===============================================================================
"""
from FreedgeDatabase import new_database_from_csv
from datetime import date

def main():
	"""
	Description: Runs the database_simulator test script.
	Returns: None
	"""
	# Create a new database from a specific CSV file to a specific location in the test_folder
	tdb = new_database_from_csv(r"test_data/fdb_needs_updating.db", "./test_data/freeedge_data_tiny.csv")
	# Retrieve the database as a list of Freedge objects
	freedges = tdb.get_freedges()
	
	# Print out information about the default-created freedges
	print("\n Default Freedge objects: \n")
	for i in range(len(freedges)):
		print(freedges[i].freedge_id, " ", freedges[i].caretaker_name, " ",
		freedges[i].last_status_update, " ", freedges[i].permission_to_notify)
	
	# Define a list of dates to be set as the last_status_update values of the freedges
	dates = ["2021-10-21", "2022-02-22", "2022-01-19", "2019-06-18", "2021-07-18",
			 "2021-12-12", "2021-12-29", "2022-01-18"]
	
	# Update the dates of the freedges to those in the generated list
	for i in range(len(freedges)):
		freedges[i].last_status_update = date.fromisoformat(dates[i])
		tdb.update_freedge(freedges[i])
	print("\n\n")
	# Print out the new freedge objects and their dates
	print("Updated Out-of-Date Freedge objects: \n")
	freedges = tdb.get_freedges()
	for f in freedges:
		print(f.freedge_id, " ", f.caretaker_name, " ", f.last_status_update, " ", f.permission_to_notify)


if __name__ == '__main__':
	main()
