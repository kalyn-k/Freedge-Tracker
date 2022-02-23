"""
===============================================================================
Title:	Constants File for the Freedge Database in the Freedge Tracker System
===============================================================================
Description:	TODO
Authors: 		TODO
Last Edited: 	2-22-2022
Last Edit By:	Madison Werries
"""
# The path for the location of the internal database file
# Default = r"..\freedge_internal_database\pythonsqlite.db"
DATABASE_PATH = r".\freedge_internal_database\freedge_database.db"

DATABASE_CSV = r".\test_data\freeedge_data_tiny.csv"

# The correct column label in the csv file for the caretaker's phone number
PHONE_NUMBER_KEY = "Phone Number"

# The correct column label in the csv file for the caretaker's email address
EMAIL_ADDRESS_KEY = 'Email Address'

# The correct label in the csv for the caretaker's notification permission flag
PERMISSION_TO_CONTACT_KEY = "Permission to Contact"

# The correct column label in the csv for the caretaker's preferred contact method
PREFERRED_METHOD_COLUMN = 'Y'

# The form response string for caretakers who want to notified via text
SMS_METHOD_STRING = "text"

# The form response string for caretakers who want to notified via email
EMAIL_METHOD_STRING = "email"

