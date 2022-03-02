"""
===============================================================================
Title:	Freedge Data Entry Class for the Freedge Tracker System
===============================================================================
Description:	TODO
Authors: 		TODO
Last Edited: 	2-22-2022
Last Edit By:	Madison Werries
"""
from enum import Enum
from datetime import date
from numpy.core.defchararray import upper
from freedge_internal_database import database_constants as dbc

class Status(Enum):
	""" An Enum class to encapsulate the potential status of a freedge. """
	Active = "active"
	SuspectedInactive = "suspected inactive"
	ConfirmedInactive = "confirmed inactive"

class ContactMethod(Enum):
	""" Options for a caretaker's preferred contact method (email/SMS). """
	SMS = dbc.SMS_METHOD_STRING
	Email = dbc.EMAIL_METHOD_STRING
	
class Freedge:
	""" A class for easily retrieving info about a freedge in the FreedgeDatabase. """
	def __init__(self, fid, pname, nname, cname, loc, last_update, c_method, phone, email,
				 installed_date, permission):
		self.freedge_id = fid
		self.project_name = pname
		self.network_name = nname
		self.caretaker_name = cname
		self.fridge_location = loc
		self.date_installed = installed_date
		self.permission_to_notify = permission
		self.preferred_contact_method = c_method
		self.phone_number = phone
		self.email_address = email
		self.freedge_status = Status.Active
		self.last_status_update = last_update
	
	def can_notify(self):
		""" Returns whether the freedge's owner has agreed to receive notifications. """
		return self.permission_to_notify
	
	def set_permission_to_notify(self, can_notify: bool):
		""" Change a freedge caretaker's notification permission status. """
		self.permission_to_notify = can_notify
	
	def set_preferred_contact_method(self, t: ContactMethod):
		""" Change a freedge caretaker's preferred contact method. """
		self.preferred_contact_method = t
	
	def time_since_last_update(self):
		""" Returns # of days since the last activity status update. """
		prev = self.last_status_update
		today = date.today()
		diff = (today-prev).days
		if (diff < 0):
			diff = 0
		return diff
	
	def update_status(self, s: Status):
		""" Updates the active status of the freedge based on today's date. """
		self.freedge_status = s
		self.reset_last_update()
	
	def reset_last_update(self):
		""" Sets last update to today's date """
		self.last_status_update = date.today()
		
	def comparison_string(self, field_name, old, new):
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
		""" Returns a list of the fields which differ between two freedges. """
		diff = []

		field_names = ['Database ID', 'Project Name', 'Network Name',
					   'Caretaker', 'Location', 'Date Installed',
					   'Permission to Notify', 'Preferred Contact Method',
					   'Phone Number', 'Email Address', 'Status',
					   'Last Status Update']
		f1 = [self.freedge_id, self.project_name, self.network_name,
			  self.caretaker_name, self.fridge_location, self.date_installed,
			  self.permission_to_notify, self.preferred_contact_method,
			  self.phone_number, self.email_address, self.freedge_status,
			  self.last_status_update]
		f2 = [f.freedge_id, f.project_name, f.network_name,
			  f.caretaker_name, f.fridge_location, f.date_installed,
			  f.permission_to_notify, f.preferred_contact_method,
			  f.phone_number, f.email_address, f.freedge_status,
			  f.last_status_update]

		for i in range(len(field_names)):
			if (f1[i] != f2[i]):
				c = self.comparison_string(field_names[i], f1[i], f2[i])
				diff.append(c)
				
		return diff
		
	def ToString(self):
		""" Converts the freedge data to a string containing the project name,
			caretaker name, and status. """
		loc = self.fridge_location
		ret = "Project name: " + self.project_name + " Caretaker: " +\
			self.caretaker_name + " Location: " + loc.state_province + ", " +\
			loc.city
		return ret

class FreedgeAddress:
	def __init__(self, loc):
		""" A class to store the address of a freedge. """
		self.street_address = loc[0]
		self.city = loc[1]
		self.state_province = loc[2]
		self.zip_code = loc[3]
		self.country = loc[4]
		
	def ToString(self):
		""" Returns a string version of the address. """
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
