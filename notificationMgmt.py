"""
===============================================================================
Title:	Notification Management
===============================================================================
Description:	TODO

Authors: 		Ellie Kobak, Liza Richars
Last Edited: 	2-24-2022
Last Edit By:	Liza Richards

Edit Log
date         editor     changes
2-17-22      lr         initial doc
2-24-22     erk         created NotificationMGMT Class
2-25-22     erk         created SMSMGMT Class


"""

import csv
import string

from twilio.rest import TwilioRestClient
from datetime import datetime
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
        #remove?
        self.sender = send_number
        self.reciever = del_number
        self.message = message

    def send_msg():
        pass
    
    def _msg_status(status = False):
        '''
        Params: status, defaults to false, but is updated to true when message is sent 
        successfully

        helper function
        '''
        return status

    def message_info():
        pass

    def timestamp()
        pass


class SMS_mgmt(NotificationMgmt):
    '''
    TODO add description
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





