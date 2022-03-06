"""
===============================================================================
Title:	Simulator for FreedgeDatabase for the Freedge Tracker System
===============================================================================
Description:	This script is for testing purposes only.

				The database simulator is used to create an imaginary database
				which includes freedges whose statuses are out-of-date (i.e.
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
from FreedgeDatabase import new_database_from_csv
from datetime import date
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
	
	# Define a list of years to be used when setting last_status_update values of the freedges
	years = [2017, 2018, 2019, 2020, 2021]
	
	# Update the dates of the freedges to randomly selected past dates (creating out-of-date freedges)
	# Every nth freedge's date will not be updated (to ensure some freedge are up-to-date)
	n = random.randint(3, 20)
	for i in range(len(freedges)):
		if (i % n != 0):
			year = random.choice(years)
			month = random.randint(1, 12)
			day = random.randint(1,28)
			freedges[i].last_status_update = date(year, month, day)
			tdb.update_freedge(freedges[i])

if __name__ == '__main__':
	main()
