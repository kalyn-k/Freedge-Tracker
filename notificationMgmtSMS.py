"""
===============================================================================
Title:	 SMS Notification Management
===============================================================================
Description:	This is skeleton code to be updated with Twilio in order to 
                send notifications via SMS. Twilio is a paid service and therefore 
                we are not using it in the prototype
                TODO add more.

Authors: 		Ellie Kobak,
Last Edited: 	2-28-2022
Last Edit By:	Ellie Kobak

Edit Log
date         editor     changes
2-28-22     erk          initial doc

"""

import csv
import string

from twilio.rest import TwilioRestClient
from datetime import datetime
from freedge_internal_database.database_constants import *
from caretaker_info_parser import *
from freedge_data_entry import *
from notificationMgmt import *

send_number = "5033199677"
del_number = "9254052580"
message = "test, test freedgeeeee"


class SMS_mgmt(NotificationMgmt):
    '''
    TODO add description

    TODO update functions to match NotificationMgmt
    '''
    def __init__():
        self.sender = send_number
        self.reciever = del_number
        self.message = message

    def send_msg():
        '''
        timestamp = 2021-07-03 16:21:12.357246
        '''
        client = TwilioRestClient()
        client.messages.create(from_=self.sender,
                       to=self.reciever,
                       body=self.message)
        return datetime.now()
    
    def _msg_status(status = False):
        '''
        Params: status, defaults to false, but is updated to true when message is sent 
        successfully

        helper function
        '''
        return status

    def message_info():
        # find way to get list of everything you need for last sent info
        pass

# load internal database, get freedge database object, all you have to do to get the information
# freedge database object.freedges

# have the classes accept the freedge database as an argument,

# expect instructor to send fridge database object or the list of freedges, most likely list of freedges

