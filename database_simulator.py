"""
===============================================================================
Title:	Simulator for FreedgeDatabase for the Freedge Tracker System
===============================================================================
Description:	This script is for testing purposes only.

				The database simulator is used to create an database of fabricated
				data that includes freedges whose statuses are out-of-date (i.e.
				their last status update was longer than the number of days
				specified at FIRST_UPDATE_THRESHOLD in the constants file,
				freedge_constants.py.)
				
===============================================================================
Instructions: How To Utilize this test script:
===============================================================================
(1)	Upon running this file, a database is first created from a csv file
	containing test data (found in test_data folder) which is formatted 
	in the way that the Freedge organization currently formats their data 
	in csv files.
	
(2)	The program then updates the created database, manually setting some of
	their last_status_update dates to be older than the out-of-date threshold.
	
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
Last Edit By:	Ginni Gallagher
===============================================================================
"""
from FreedgeDatabase import new_database_from_csv, freedge_data_entry
from InternalData import freedge_constants
from datetime import date, timedelta
import random

def main():
	"""
	Description: Runs the database_simulator test script.
	Returns: None
	"""
	# Create a new database from a specific CSV file to a specific location in the test_folder
	tdb = new_database_from_csv(r"test_data/fdb_needs_updating.db", "./test_data/freeedge_data.csv")
	# Retrieve the database as a list of Freedge objects
	freedges = tdb.get_freedges()

	# Get current date to use in determining the activity status of an out-of-date freedge
	current_date = date.today()
	
	# Update every nth freedge's date to be out-of-date
	n = random.randint(4, 10)
	for i in range(len(freedges)):

		# Update the nth freedge's date
		if (i % n == 0):
			# Randomly generate days since last update (up to two years from current date) 
			days_since_update = timedelta(random.randint(1, 730))
			out_of_date = current_date - days_since_update

			freedges[i].last_status_update = out_of_date

			# if freedge date is past {FIRST_UPDATE_THRESHOLD} days since last update, 
			# update activity status to "SuspectedInactive"
			days_since_update = current_date - out_of_date
			if (days_since_update.days > freedge_constants.FIRST_UPDATE_THRESHOLD):
				freedges[i].freedge_status = freedge_data_entry.Status.SuspectedInactive

			tdb.update_freedge(freedges[i])


if __name__ == '__main__':
	main()
