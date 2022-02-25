"""
===============================================================================
Title:	Notification Management
===============================================================================
Description:	TODO

Authors: 		Ellie Kobak, Liza Richars
Last Edited: 	2-24-2022
Last Edit By:	Liza Richards
"""

import csv
import string
import twilio.rest import TwilioRestClient

from freedge_internal_database.database_constants import *
from caretaker_info_parser import *
from freedge_data_entry import *

send_number = "5033199677"
del_number = "9254052580"
message = "test, test freedgeeeee"


class NotificationMgmt():
    '''
    TODO add description
    '''
    def __init__():
        self.sender = send_number
        self.reciever = del_number
        self.message = message

    def send_sms():
        client = TwilioRestClient()
        client.messages.create(from_=self.sender,
                       to=self.reciever,
                       body=self.message)

# load internal database, get freedge database object, all you have to do to get the information
# freedge database object.freedges

# have the classes accept the freedge database as an argument,

# expect instructor to send fridge database object or the list of freedges, most likely list of freedges





