"""
===============================================================================
Title:	Constants File for the Freedge Database in the Freedge Tracker System
===============================================================================
Description:	TODO
Authors: 		TODO
Last Edited: 	2-22-2022
Last Edit By:	Madison Werries
"""
#==============================================================================
# Constants for how often to check in with Freedge Caretakers
#==============================================================================
# Desired threshold for the number of days since the last status update where
# we would like to get a status update from the freedge caretaker again.
FIRST_UPDATE_THRESHOLD = 90
# Time before a freedge's status automatically switches to 'Suspected Inactive'
SECOND_UPDATE_THRESHOLD = 365

#==============================================================================
# Paths to the internal database_manager file
#==============================================================================
# The path for the location of the internal database_manager file
DATABASE_PATH_INFO = r"internal_data/fdb_path.txt"

#=============================================================================
# CSV File Column Labels/Headers
#==============================================================================
# The column label in the csv file for the freedge's project name
PROJECT_NAME_KEY = "Project"

# The column label in the csv file for the freedge's network name
NETWORK_NAME_KEY = "Network"

# The column label in the csv file for the street address of the freedge
STREET_ADDRESS_KEY = "Street address"

# The column label in the csv file for the city of the freedge
CITY_KEY = "City"

# The column label in the csv file for the state/province of the freedge
STATE_PROVINCE_KEY = "State / Province"

# The column label in the csv file for the zip code of the freedge
ZIP_CODE_KEY = "Zip Code"

# The column label in the csv file for the country the freedge is in
COUNTRY_KEY = "Country"

# The column label in the csv file for the date the freedge was installed
DATE_INSTALLED_KEY = "Date Installed"

# The column label in the csv file for the main contact (caretaker's) name
CONTACT_NAME_KEY = "Contact Name"

# The correct column label in the csv file for the caretaker's phone number
PHONE_NUMBER_KEY = "Phone Number"

# The correct column label in the csv file for the caretaker's email address
EMAIL_ADDRESS_KEY = 'Email Address'

# The correct label in the csv for the caretaker's notification permission flag
PERMISSION_TO_CONTACT_KEY = "Permission to Contact"

# The column label in the csv for the caretaker's preferred contact method
PREFERRED_METHOD_KEY = "Preferred Contact Method"

# The column label in the csv file for the freedge's active/inactive status
ACTIVE_STATUS_KEY = "Active?"
#==============================================================================

# The form response string for caretakers who want to notified via text
SMS_METHOD_STRING = "text"

# The form response string for caretakers who want to notified via email
EMAIL_METHOD_STRING = "email"

