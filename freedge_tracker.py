"""
===============================================================================
Title:	Main Driver for the Freedge Tracker System
===============================================================================
Description:	This is the main driver for the Freedge Tracker System. Its
				primary interactions are with the admin_interface module
				to start the program.
                
Authors:        Madison Werries
Last Edited:    3-5-2022
Last Edit By:   Madison Werries
"""
from database import *
from admin_interface.administrator_interface import *

def main():
	# Create a new Administrator Interface
	MainInterface = AdministratorInterface()
	# Build the Administrator Interface's GUI
	MainInterface.CreateDisplay()
	
	# Check whether or not an internal database already exists. This
	# information is stored using the file: "internal_data/fdb_path.txt"
	try:
		# Check that the file "internal_data/fdb_path.txt" exists
		path_location = open(DATABASE_PATH_INFO, "r")
	except IOError:
		# If there's an error and the internal file does not exist, create it
		path_location = open(DATABASE_PATH_INFO, "w+")
		# Write a header briefly describing the file
		path_location.write("This is a text file which contains the file path"
							" to the last database (.db file) that was opened.")
		# Write a blank line to be filled with the file path later
		path_location.write("")
	
	# Read the lines in from the internal file
	lines = path_location.readlines()
	db_file_found = False  # Whether we successfully find a .db file
	located_file_path = ""  # The path to the .db file, if one is found
	path_location.close()
	# If the number of lines is less than 2, there is no file path specified
	if (len(lines) >= 2):
		# The first line is the header, the second is the file location
		located_file_path = lines[1]
		db_file_found = exists_internal_database(located_file_path)
	
	# Ensure that the dialogue boxes will be shown
	MainInterface.root.update()
	
	# If an internal database file was found...
	if (db_file_found):
		# Prompt the user for whether they want to use the (.db) file found
		title = "An existing database was found at: " + located_file_path + \
				".\n\nWould you like to proceed with that database?"
		proceed_response = messagebox.askyesno("Database Found", title)
		# If they gave a response (ie, didn't just hit 'X')...
		if (proceed_response is not None):
			if proceed_response:
				# Otherwise, load the internal database file that was found
				MainInterface.fdb_path = located_file_path
				MainInterface.LoadDatabase(located_file_path)
	MainInterface.UpdateFullDisplay()
	MainInterface.root.mainloop()
		

if __name__ == '__main__':
	main()
