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
	
class FreedgeAddress:
	def __init__(self, street, city, state_prov, zcode, country, loc_type=""):
		""" A class to store the address of a freedge. """
		self.street_address = street
		self.city = city
		self.state_or_province = state_prov
		self.zip_code = zcode
		self.country = country
		self.location_type = loc_type

class Freedge:
	""" A class for data entries in the Freedge Database. """
	def __init__(self, pname, cname, loc, c_method, phone, email,
				 installed_date, permission=False, sensor_exists=False):
		self.project_name = pname
		self.caretaker_name = cname
		self.fridge_location = loc
		self._permission_to_notify = permission
		self.preferred_contact_method = c_method
		self.phone_number = phone
		self.email_address = email
		self.freedge_status = Status.Active
		self.last_status_update = installed_date
		self.has_fridge_sensor = sensor_exists
	
	def can_notify(self):
		""" Returns whether the freedge's owner has agreed to receive notifications. """
		return self._permission_to_notify
		
	def set_permission_to_notify(self, can_notify: bool):
		""" Change a freedge caretaker's notification permission status. """
		self._permission_to_notify = can_notify
		
	def set_preferred_contact_method(self, t: ContactMethod):
		""" Change a freedge caretaker's preferred contact method. """
		self.preferred_contact_method = t
		
	def time_since_last_update(self):
		""" Returns # of days since the last activity status update. """
		prev = self.last_status_update
		today = date.today()
		return today - prev
	
	def update_status(self, s: Status):
		""" Updates the active status of the freedge. """
		self.freedge_status = s
		self.reset_last_update()
		
	def reset_last_update(self):
		""" Sets last update to today's date """
		self.last_status_update = date.today()
