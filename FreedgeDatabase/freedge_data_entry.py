"""
===============================================================================
Title:	Freedge Data Entry Class for the Freedge Tracker System
===============================================================================
Description:	Holds Freedge class and Freedge Address class constructors.
		Freedge objects are used store location-specific information
		for each freedge in the system. Additional information is 
		stored in a freedge object, such as the current status of
		the freedge (active or inactive) and the preferred method
		of contact for reaching the freedge caretaker (SMS or email).

		Freedge objects are added and stored in the FreedgeDatabase.

Authors: 	Madison Werries, Ginni Gallagher
Last Edited: 	3-6-2022
Last Edit By:	Madison Werries
"""
from enum import Enum
from datetime import date 
from InternalData import freedge_constants as dbc

class Status(Enum):
	""" 
	An Enum class to encapsulate the current known status of a freedge. 

	Defined Enum Constants (keys):
	-----------------------------
	Active:
		Status.Active indicates that the status of a given freedge is known to
		be active. This means the freedge's status has been updated within the
		last {FIRST_UPDATE_THRESHOLD} days.
			  
	SuspectedInactive:
		Status.SuspectedActive indicates that the status of the freedge is
		LIKELY to be inactive. This happens when the freedge's status has not
		been updated within the last {FIRST_UPDATE_THRESHOLD} days, and the
		user has neither confirmed nor denied that their freedge is inactive.
		
	ConfirmedInactive:
		Status.ConfirmedInactive indicates that the status of the freedge is known
		to be inactive. This means that the freedge caretaker at some point
		notified the system that their freedge is inactive.
		
	Unknown:
		 Status.Unknown indicates that the status of the freedge is not
		 known at this time. It differs from 'SuspectedInactive' in that a
		 freedge's status cannot reasonably be defined as 'SuspectedInactive' if
		 a caretaker has not given consent to receive notifications.
		 
		 When creating a new database from a CSV file, this is the default
		 Status assigned when both the {ACTIVE_STATUS_KEY?} column and the
		 {PERMISSION_TO_CONTACT_KEY} column have been left blank.
	"""
	# The caretaker's status is known
	Active = "ACTIVE"
	Unknown = "UNKNOWN"
	SuspectedInactive = "SUSPECTED INACTIVE"
	ConfirmedInactive = "CONFIRMED INACTIVE"

class ContactMethod(Enum):
	""" 
	Options for a caretaker's preferred contact method. This preference is
	determined by what mode of contact was indicated by the user on the inputted
	csv file.

	Defined Enum Constants (keys):
	-----------------------------
	SMS -> a constant (defined as a string in freedge_constants.py) indicating
			the freedge caretaker prefers text notifications
	Email -> a constant (defined as a string in freedge_constants.py) indicating
			the freedge caretaker prefers email notifications
	"""
	SMS = dbc.SMS_METHOD_STRING
	Email = dbc.EMAIL_METHOD_STRING
	
class Freedge:
	""" 
	A class containing information about a particular freedge in the FreedgeDatabase. 
	
	Attributes
	-----------
	freedge_id -> a string of the id assigned to the freedge for use in database
	project_name -> a string of the name of the specific freedge
	network_name -> a string of the name of the organizer of the freedge
	caretaker_name -> a string of the name of the freedge caretaker
	fridge_location -> a string of the location of the freedge
	date_installed -> a string of the date the freedge was installed
	permission_to_notify -> a string indicating the freedge caretaker gave permission to receive notifications
	preferred_contact_method -> a string indicating the freedge caretaker's preferred method of contact
	phone_number -> a string of the caretaker's phone number
	email_address -> a string of the caretaker's email address
	freedge_status -> a string defined in Status class indicating freedge's status
	last_status_update -> a string of the last date a status update was received

	Methods
	--------
	can_notify(): Returns whether or not freedge caretaker has agreed to receive notifications

	set_permission_to_notify(can_notify): Change the freedge caretaker notification permission status

	set_preferred_contact_method(t): Change the freedge caretaker's preferred contact method
	
	time_since_last_update(): Returns number of days since last status update

	update_status(s): Update the status of the freedge

	reset_last_update(): Reset the last update attribute to current date

	comparison_string(field_name, old, new): Returns a string comparing a freedge's old field
											to the updated field 
	
	compare_freedges(f): Compares two freedges and returns a list of fields that differ

	ToString(): Converts the freedge data to a string containing the project name,
				caretaker name, and status.
	"""
	def __init__(self, fid, pname, nname, cname, loc, last_update, c_method, phone, email,
				 installed_date, permission):
		"""
		Initializes the information read in by the input csv file for each freedge.
		"""
		self.freedge_id = fid
		self.project_name = pname
		self.network_name = nname
		self.caretaker_name = cname
		self.fridge_location = loc
		if (installed_date == "-"):
			self.date_installed = None
		else:
			self.date_installed = installed_date
		self.permission_to_notify = permission
		self.preferred_contact_method = c_method
		self.phone_number = phone
		self.email_address = email
		self.freedge_status = Status.Active
		if (last_update == "-"):
			self.last_status_update = None
		else:
			self.last_status_update = last_update
		
		#if (last_update.isoformat() != "0000-00-00"):
		
	
	def can_notify(self):
		""" 
		Returns whether the freedge's owner has agreed to receive notifications. 
		
		Paramters: None

		Returns: True or False
		"""
		return self.permission_to_notify
	
	def set_permission_to_notify(self, can_notify: bool):
		""" 
		Change a freedge caretaker's notification permission status. 
		
		Parameters: can_notify -> a bool indicating if freedge caretaker gave notification permission

		Returns: None
		"""
		self.permission_to_notify = can_notify
	
	def set_preferred_contact_method(self, t: ContactMethod):
		""" 
		Change a freedge caretaker's preferred contact method. 
		
		Parameters: t -> a string of the preferred contact method

		Returns: None
		"""
		self.preferred_contact_method = t
	
	def time_since_last_update(self):
		""" 
		Returns # of days since the last activity status update. 
		
		Parameters: None

		Returns:
			diff -> an int representing days since the freedge's last status
					update. If the freedge_status is Unknown (likely because
					the freedge was just created from a CSV where the status of
					the freedge has never been updated before and the caretaker
					has not given contact permission, return None.
		"""
		if (self.freedge_status == Status.Unknown):
			return None
		if (self.last_status_update is None):
			return None
		prev = self.last_status_update
		today = date.today()
		diff = (today-prev).days
		if (diff < 0):
			diff = 0
		return diff
	
	def update_status(self, s: Status):
		""" 
		Updates the active status of the freedge based on today's date. 
		
		Parameters: s -> a string indicating the updated status of the freedge

		Returns: None
		"""
		self.freedge_status = s
		self.reset_last_update()
	
	def reset_last_update(self):
		""" 
		Sets last update to today's date 
		
		Parameters: None

		Returns: None
		"""
		self.last_status_update = date.today()
		
	def comparison_string(self, field_name, old, new):
		"""
		Compares a specified field between old and new freedge information.

		Parameters:
			field_name -> a string of the field name to be compared
			old -> a string of the freedge's old data for the fieldname specified
			new -> a string of the freedge's new data for the fieldname specified

		Returns: ret -> a formatted string describing the comparison
		"""
		if (field_name == 'Location'):
			ret = field_name + "\n"
			ret += "Old: " + old.ToString()
			ret += "New: " + new.ToString()
		else:
			ret = field_name + "\n"
			ret += "Old: " + old
			ret += "New: " + new
		return ret
		
	def compare_freedges(self, f):
		""" 
		Returns a list of the fields which differ between two freedges. 
		
		Parameters: f -> a Freedge object

		Returns: diff -> a formatted string describing the comparison
		"""
		diff = []

		field_names = ['Database ID', 'Project Name', 'Network Name',
					   'Caretaker', 'Location', 'Date Installed',
					   'Permission to Notify', 'Preferred Contact Method',
					   'Phone Number', 'Email Address', 'Status',
					   'Last Status Update']

		# attributes for the first freedge object
		f1 = [self.freedge_id, self.project_name, self.network_name,
			  self.caretaker_name, self.fridge_location, self.date_installed,
			  self.permission_to_notify, self.preferred_contact_method,
			  self.phone_number, self.email_address, self.freedge_status,
			  self.last_status_update]

		# attributes for the second freedge object
		f2 = [f.freedge_id, f.project_name, f.network_name,
			  f.caretaker_name, f.fridge_location, f.date_installed,
			  f.permission_to_notify, f.preferred_contact_method,
			  f.phone_number, f.email_address, f.freedge_status,
			  f.last_status_update]

		# compare each field between the freedge objects, looking for differences
		for i in range(len(field_names)):
			if (f1[i] != f2[i]):
				c = self.comparison_string(field_names[i], f1[i], f2[i])
				diff.append(c)
				
		return diff
		
	def ToString(self):
		"""
		Converts the freedge data to a string containing the project name,
		caretaker name, and status.
		 
		Parameters: None

		Returns: ret -> a formatted string describing the freedge location 
		"""
		ret = "Database ID:\t" + str(self.freedge_id)
		ret += "\nProject Name:\t" + self.project_name
		ret += "\nNetwork Name:\t" + self.network_name
		ret += "\nCaretaker:\t" + self.caretaker_name
		ret += "\nFridge Location:\t" + self.fridge_location.ToDisplayString()
		ret += "\nDate Installed:\t" + str(self.date_installed)
		ret += "\nMay Notify?:\t" + str(self.permission_to_notify)
		ret += "\nPreferred Contact:\t" + self.preferred_contact_method
		ret += "\nPhone Number:\t" + self.phone_number
		ret += "\nEmail Address:\t" + self.email_address
		ret += "\nFridge Status:\t" + str(self.freedge_status.value)
		ret += "\nLast status update:\t" + str(self.last_status_update)
		ret += "\nDays since last update:\t" + str(self.time_since_last_update())
		return ret

class FreedgeAddress:
	"""
	A class to contain the address information of a freedge.

	Attributes
	-----------
	street_address -> a string of the freedge's street address
	city -> a string of the freedge's city
	state_province -> a string of the freedge's state
	zip_code -> a string of the freedge's zip code
	country -> a string of the freedge's country

	Methods
	-------
	ShortString()
		Returns the freedge's city and state
		
	ToString()
		Returns the freedge's full address on a single line
		
	ToDisplayString()
		Returns the freedge's full address, formatted to display
		oneattribute per line
	"""
	def __init__(self, loc):
		""" 
		A constructor to store the address of a freedge. 

		Parameters: loc -> a list of strings of a freedge's address

		Returns: None
		"""
		self.street_address = loc[0]
		self.city = loc[1]
		self.state_province = loc[2]
		self.zip_code = loc[3]
		self.country = loc[4]
		
	def ShortString(self):
		""" 
		Returns a string of the freedge's address in a concise display format.
		
		Parameters: None
		Returns: ret -> a string
		
		The formats returned by the parser are based on which fields exist,
		and may be of any of the following forms listed below:
			(1) '{city}, {state/province}, {country}'
			(2) '{city}, {state/province}'
			(3) '{city}, {country}'
			(4) '{country}'
			(5) '{city}
			(6) 'NOT GIVEN'
		"""
		has_city = (len(self.city.strip())) != 0
		has_state = (len(self.state_province.strip())) != 0
		has_country = (len(self.country.strip())) != 0
		
		# Format (1): '{city}, {state/province}, {country}'
		if (has_city and has_state and has_country):
			return self.city + ", " + self.state_province + ", " + self.country
		# Format (2): '{city}, {state/province}'
		elif (has_city and has_state and not has_country):
			return self.city + ", " + self.state_province
		# Format (3): '{city}, {country}'
		elif (has_country and has_city and not has_state):
			return self.city + ", " + self.country
		# Format (4): '{country}'
		elif (has_country and not has_city and not has_state):
			return self.country
		# Format (5): '{city}'
		elif (has_city and not has_state and not has_country):
			return self.city
		# Format (6): 'NOT GIVEN'
		else:
			return "NOT GIVEN"
		
	def ToString(self):
		""" 
		Returns a full single-line string of the freedge's address.
		
		Parameters: None

		Returns: ret -> a string
		"""
		ret = ""
		if (self.street_address != ""):
			ret += self.street_address + ", "
		if (self.city != ""):
			ret += self.city + ", "
		if (self.state_province != ""):
			ret += self.state_province + ", "
		if (self.zip_code != ""):
			ret += self.zip_code + ", "
		if (self.country != ""):
			ret += self.country
		return ret
	
	def ToDisplayString(self):
		"""
		Returns a full string of the freedge's address, formatted for display.

		Parameters: None

		Returns: ret -> a string
		"""
		ret = ""
		if (self.street_address != ""):
			ret += self.street_address + "\n\t\t"
		if (self.city != ""):
			ret += self.city + ", "
		if (self.state_province != ""):
			ret += self.state_province + ", "
		if (self.zip_code != ""):
			ret += self.zip_code + " "
		if (self.country != ""):
			ret += "\n\t\t" + self.country
		return ret
