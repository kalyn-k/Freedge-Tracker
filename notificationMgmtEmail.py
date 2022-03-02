"""
===============================================================================
Title:	 Email Notification Management
===============================================================================
Description:	This is skeleton code to be updated with Twilio in order to 
                send notifications via email. Twilio is a paid service and therefore 
                we are not using it in the prototype. 

                The email system will function through inheriting the notification class.
                The NotificationMgmt is created using modularity so any future notification
                type can be added without touching the main NotificationMgmt file. In order
                for a future developer to implement emailing, they will need to add to implement
                the notify_and_update function within the class.

                Information on Twilio for setting up email:
                Payment plans:
                https://www.twilio.com/sendgrid/email-api

                Instruction use and sample code:
                https://www.twilio.com/docs/verify/email
        
                TODO is this good?

Authors: 		Ellie Kobak,
Last Edited: 	3-01-22
Last Edit By:	Ellie Kobak

Edit Log
date         editor     changes
2-28-22      erk        initial doc
3-01-22      erk        documentation
"""

from twilio.rest import TwilioRestClient    # Twilio extension to send email 

from datetime import datetime               # used to update date
from freedge_internal_database.database_constants import * # acc
from caretaker_info_parser import *
from freedge_data_entry import *    # 
from notificationMgmt import *      # main class definition


class email_mgmt(NotificationMgmt):
    '''
    TODO add description

    TODO update functions to match NotificationMgmt
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
        