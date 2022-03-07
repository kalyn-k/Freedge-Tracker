"""
===============================================================================
Title:	Constants File for the Freedge Database in the Freedge Tracker System
===============================================================================
Description:	A list of constants for the Freedge Tracker System. These
				constants may be modified by the administrator users in order
				to suit the needs of the system. Information about the default
				values and the reasonable expected values of the constants is
				detailed in the Programmer_Documentation.pdf document.
				
Authors: 		Madison Werries
Last Edited: 	03-06-2022
Last Edit By:	Ginni Gallagher
"""
#==============================================================================
# Constants for how often to check in with Freedge Caretakers
#==============================================================================
# Desired threshold for the number of days since the last status update where
# we would like to get a status update from the freedge caretaker again.
FIRST_UPDATE_THRESHOLD = 90

#==============================================================================
# Internal Data Constants
#==============================================================================
# The path to the text file which contains the path of the most recently loaded
# database file (.db). This is used to prompt the user on startup about the
# last database which was loaded.
# DEFAULT: {r"InternalData/fdb_path.txt"}
DATABASE_PATH_INFO = r"InternalData/fdb_path.txt"

#=============================================================================
# CSV File Column Labels/Headers
#==============================================================================
# Description: The following constants define the string names of the headers
# within the CSV files to be loaded into the system. While the names can be
# safely changed, always ensure that any CSV column names which are to be
# loaded into the system are also updated to match these constants EXACTLY.

# !!! IMPORTANT: DO NOT DELETE ANY OF THE HEADERS !!!
#==============================================================================
PROJECT_NAME_KEY = "Project"
NETWORK_NAME_KEY = "Network"

STREET_ADDRESS_KEY = "Street address"
CITY_KEY = "City"
STATE_PROVINCE_KEY = "State / Province"
ZIP_CODE_KEY = "Zip Code"
COUNTRY_KEY = "Country"

DATE_INSTALLED_KEY = "Date Installed"

CONTACT_NAME_KEY = "Contact Name"
PHONE_NUMBER_KEY = "Phone Number"
EMAIL_ADDRESS_KEY = 'Email Address'

PERMISSION_TO_CONTACT_KEY = "Permission to Contact"
PREFERRED_METHOD_KEY = "Preferred Contact Method"

ACTIVE_STATUS_KEY = "Active?"

#==============================================================================
# CSV File Notification Method Constants

# Description:
# These two contants define the VALUES to be in the rows of the CSV file in
# order to parse a caretaker's preferred contact method. That is, underneath
# the column named {PREFERRED_CONTACT_METHOD}, the system expects to find
# {SMS_METHOD_STRING} OR {EMAIL_METHOD_STRING}.
#==============================================================================
SMS_METHOD_STRING = "text"
EMAIL_METHOD_STRING = "email"
