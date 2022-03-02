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
import string
from typing import no_type_check       #

from twilio.rest import TwilioRestClient
from datetime import datetime
from freedge_internal_database.database_constants import *
import caretaker_info_parser
import freedge_data_entry
import freedge_database
import notificationGUI      # for prototype only, used for popup display of notification


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
        Purpose:
            This function obtains which freedges are out of date (have not had a status update in 90 days),
            collects the freedge's caretaker, name, and time since last update to be used to craft a message for the 
            notification GUI. The function also update the freedge object's status based on user response, and then 
            further update the freedge database.

        Parameters: None
       
        Calls:
            called by: XXX when system has not been notified of activity in 90 days,
                     notify_and_update() to send notification
           
        Returns: caretaker_name -> string of name of caretaker, 
                 project_name -> string of name of fridge project,
                 last_update -> integer of date of last update

        Inputs: None
        Returns: caretaker_name, project_name, last_update
        '''
        project_name = ''       # initalializes variable for project name
        caretaker_name = ''     # initalializes variable for caretaker name
        last_update = 0         # initalializes variable to store last update

        # call to the other classes in order to use their methods
        fdb = freedge_database.FreedgeDatabase()  # freedge database class initialization
        f = freedge_data_entry.Freedge()         # actual fridge class initialization

        fridge_list = fdb.get_out_of_date()  # variable to obtain the list of freedge objects that are out of date


        # Iterates through list of freedge objects and obtains the caretaker's name, project name, and time since
        # last update. These three items will be returned by the function to be used to craft a message to the
        # caretaker through the notification GUI.
        for fridge in fridge_list:
            if f.can_notify is True:
                project_name = f.project_name               # variable for project name
                caretaker_name = f.caretaker_name           # variable for caretaker name
                last_update = fdb.time_since_last_update()  # variable for time of last update
                self.notify_and_update(f, fdb, project_name, caretaker_name, last_update)

                # now set up the message with this information.
                # message = f'Hi {caretaker_name}! We noticed that {project_name} has not been updated in {last_update} days' \
                #           f'Is your Freedge still active?'

        return 


    def notify_and_update(self, freedge, fdb, project_name, caretaker_name, last_update):
        '''
        Purpose: 
            Calls the notification interface class which will return a boolean value based on whether or not the
            Freedge is active from user input.
            Based on this boolean value, updates the freedge object status and then updates the freedge database status
            for the specific fridge object.

        Parameters: 
            caretaker_name -> str
            project_name -> str
            last_update -> int?

        Calls: notificationGUI.py in order to notify user of fridge activity
            update_status() of Freedge class

        Called by: get_fridge_info_message

        Returns: None
        
        '''
        # calls notificatio GUI pop up function to send message
        popup = notificationGUI.Pop_up(project_name, caretaker_name, last_update)
        response = popup.selected_button    # variable with boolean value of activity notification response


        # call to the other classes in order to use their methods
        # TODO - note from Ellie - what does this do? if we need the fridge we should pass it in not make a new object
        fdb = freedge_database.FreedgeDatabase() 
        freedge = freedge_data_entry.Freedge()
        
        # if fridge is still active, updates fridge
        if response:
            freedge.update_status()                       # updates activity status with new time
            fdb.update_freedge(freedge.update_freedge())  # updates fridge database with new activity update



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





