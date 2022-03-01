"""
===============================================================================
Title:	notificationMgmt.py
===============================================================================
Description:	Obtains which freedges in the database are considered out of date and collects their associated
                data (caretaker name, project name, and time since last update) to be used when crafting a
                notification message by the notification GUI. Also uses the user response from the GUI to then
                update the status of the Freedge in the database.

Authors: 		Ellie Kobak, Liza Richards
Creation Date:  February 17, 2022
Last Edited: 	2-24-2022
Last Edit By:	Liza Richards

Called By:
    Notification GUI -



Edit Log
date         editor     changes
2-17-22      lr         initial doc
2-24-22     erk         created NotificationMGMT Class
2-25-22     erk         created SMSMGMT Class
2-28-22     ljr         got rid of send_msg in SMS_Mgmt class, updated the get_fridge_info_message function in the
                        NotificationMgmt Class to go through the out of date fridge objects and obtain each fridge's
                        information in order to send a message
2-28-22     erk         Added the notify function to interact with a notification GUI component that will get user
                        input to update the status of each fridge that was originally out of date.




"""

import csv          # used to implement reading from csv files
import string       #

from twilio.rest import TwilioRestClient
from datetime import datetime
from freedge_internal_database.database_constants import *
from caretaker_info_parser import *
from freedge_data_entry import *
from freedge_database import *


#message = "Hi {}, we noticed that {} has not been update in {} days. Is this Freedge still active?"


class NotificationMgmt():
    '''
    TODO add description
    '''
    def __init__(self):
        #remove?
        self.sender = send_number
        self.reciever = del_number
        self.message = message
        # NotificationMgmt.get_freedges()?
        # FreedgeDatabase.get_freedges()?
        fridge_list = []

    def get_fridge_info_message(self):
        '''
        Obtains which freedges are out of date (have not had a status update in 90 days).
        Collects the freedge's caretaker, name, and time since last update to be used to craft a message in the
        notification GUI.
        Update the freedge object's status based on user response, and then further update the freedge database.


        Inputs: None
        Returns: caretaker_name, project_name, last_update
        Called by:

        '''
        project_name = ''
        caretaker_name = ''
        last_update = 0

        # call to the other classes in order to use their methods
        fdb = freedge_databse.FreedgeDatabase()
        f = freedge_data_entry.Freedge()

        # obtain the list of freedge objects that are out of date
        fridge_list = fdb.get_out_of_date()

        # iterate through this list of freedge objects and obtain the caretaker's name, project name, and time since
        # last update. These three items will be returned by the function to be used to craft a message to the
        # caretaker through the notification GUI.
        for fridge in fridge_list:
            if f.can_notify is True:
                project_name = f.project_name
                caretaker_name = f.caretaker_name
                last_update = fdb.time_since_last_update()
                # phone = fdb.phone_number
                # method = fdb.preferred_contact_method  # will be the prototype pop up

                # now set up the message with this information.
                # message = f'Hi {caretaker_name}! We noticed that {project_name} has not been updated in {last_update} days' \
                #           f'Is your Freedge still active?'

        return project_name, caretaker_name, last_update



    def notify_and_update(self):
        '''
        Calls the notification interface which will return a boolean value based on whether or not the
        Freedge is active.
        Based on this boolean value, updates the freedge object status and then updates the freedge database status
        for the specific fridge object.

        Inputs: None
        Returns: None
        Called by:

        '''
        # call Kalyns function to the GUI pop up function which returns true or false

        # call to the other classes in order to use their methods
        fdb = freedge_databse.FreedgeDatabase()
        freedge = freedge_data_entry.Freedge()

        if response:
            freedge.update_status()
            fdb.update_freedge(update_freedge)



    # def response(self, status = False):
    #     '''
    #     Params: status, defaults to false, but is updated to true when message is sent
    #     successfully
    #
    #     helper function
    #     '''
    #     return status

    # def message_info(self):
    #     pass
    #
    # def timestamp(self):
    #     pass



#
# class SMS_mgmt(NotificationMgmt):
#     '''
#     TODO add description
#     '''
#
#     def __init__(self):
#         self.sender = send_number
#         # self.sender = send_number
#         # self.reciever = del_number
#         # self.message = message
#
#     def send_msg(self):
#         '''
#         timestamp = 2021-07-03 16:21:12.357246
#         '''
#         client = TwilioRestClient()
#         client.messages.create(from_=self.sender,
#                        to=self.reciever,
#                        body=self.message)
#         return datetime.now()
#
#     def _msg_status(self, status = False):
#         '''
#         Params: status, defaults to false, but is updated to true when message is sent
#         successfully
#
#         helper function
#         '''
#         return status
#
#     def message_info(self):
#         # find way to get list of everything you need for last sent info
#         pass

# load internal database, get freedge database object, all you have to do to get the information
# freedge database object.freedges

# have the classes accept the freedge database as an argument,

# expect instructor to send fridge database object or the list of freedges, most likely list of freedges





