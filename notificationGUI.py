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
from notificationMgmt import *

caretaker_name = "Liza"
project_name = "Sample Fridge"
last_update = "02-28-2022 17:04:58"
message = f'Hello {caretaker_name}, {project_name} has was last determined as active on {last_update}. Is this fridge still active? Please reply YES or NO'



def sent_message(caretaker_name, project_name, last_update, message):
	'''
	TODO
	'''
	pop_up = Toplevel()
	pop_up.geometry("150x30")
	# Yes button
	yes_button = Button(pop_up, text="Yes")
	yes_button.place(x=10,y=15)
	# No button
	no_button = Button(pop_up, text="No")
	no_button.place(x=20,y=15)
