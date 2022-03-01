"""
===============================================================================
Title:	Notification GUI
===============================================================================
Description:	TODO

Authors: 		Ellie Kobak, Liza Richars
Last Edited: 	2-28-2022
Last Edit By:	Liza Richards

Edit Log
date         editor     changes
2-28-22      erk         initial doc

"""

from tkinter import *
from notificationMgmt.py import *

caretaker_name = "Liza"
project_name = "Sample Fridge"
last_update = "02-28-2022 17:04:58"
message = f'Hello {caretaker_name}, {project_name} was last determined as active on {last_update}. Is this fridge still active? Please reply YES or NO'

def sent_message(caretaker_name, project_name, last_update):
	'''
	TODO
	'''
	popup = Toplevel()

	return False


