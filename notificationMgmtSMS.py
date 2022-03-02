"""
===============================================================================
Title:	 SMS Notification Management
===============================================================================
Description:	This is skeleton code to be updated with Twilio in order to 
                send notifications via SMS. Twilio is a paid service and therefore 
                we are not using it in the prototype. 

                The SMS system will function through inheriting the notification class.
                The NotificationMgmt is created using modularity so any future notification
                type can be added without touching the main NotificationMgmt file. In order
                for a future developer to implement texting, they will need to add to implement
                the notify_and_update function within the class.

                Information on Twilio for setting up SMS:
                Payment plans:
                https://www.twilio.com/sms

                Instruction use and sample code:
                https://www.twilio.com/docs/sms#get-started

Authors: 		Ellie Kobak,
Last Edited: 	3-02-22
Last Edit By:	Ellie Kobak

Edit Log
date         editor     changes
2-28-22      erk        initial doc
3-02-22      erk        documentation
"""

from twilio.rest import TwilioRestClient    # Twilio extension to send SMS 

from datetime import datetime               # used to update date
import freedge_internal_database.database_constants  # used to access constants for fridge object
import caretaker_info_parser   # used to get contact information for each fridge
import freedge_data_entry      # used to access fridge object for data information 
import freedge_database        # used to access the freedge database methods
import notificationMgmt        # main class definition
 

class sms_mgmt(notificationMgmt.NotificationMgmt):
    '''
    This class enables SMS notifications from freedge organizers to the fridge caretakers.
    The classhas the attributes to send SMS using the Twilio SMS API
    '''

    def __init__(self):
        """
        This function is set up to be updated for non prototype version.

        Parameters:  None

        Purpose:  initialize email management system to enable email communication between freedge organizers  and caretaker

        Calls:  In funtioning version, will call freedge_data_entry.py in order to obtain correct contact 
                info for each fridge.
        Returns: None, stores sender and reciever information in class initiation.
        """

        # self.sender =  UPDATE with Twilio account information
        # self.reciever = UPDAtE with freedge_data_entry
 

    def get_fridge_info_message(self):
        '''
        This function obtains which freedges are out of date (have not had a status update in 90 days),
        collects the freedge's caretaker, name, and time since last update to be used to craft a message to be 
        emailed. The function also update the freedge object's status based on user response, and then further 
        update the freedge database.

        Parameters: None
        Calls:
            called by: admin_interface.py when system has not been notified of activity in 90 days,
                     notify_and_update() to send SMS
           
        Returns: caretaker_name -> string of name of caretaker, 
                 project_name -> string of name of fridge project,
                 last_update -> integer of date of last update

        '''
        project_name = ''       # initalializes variable for project name
        caretaker_name = ''     # initalializes variable for caretaker name
        last_update = 0         # initalializes variable to store last update

        # call to the other classes in order to use their methods
        fdb = freedge_database.FreedgeDatabase()  # freedge database class initialization
        f = freedge_data_entry.Freedge()         # actual fridge class initialization

        fridge_list = fdb.get_out_of_date() # variable to obtain the list of freedge objects that are out of date

        # iterate through this list of freedge objects and obtain the caretaker's name, project name, and time since
        # last update. These three items will be returned by the function to be used to craft a message to the
        # caretaker through the notification GUI.
        for fridge in fridge_list:
            if f.can_notify is True:
                project_name = f.project_name               # variable for project name
                caretaker_name = f.caretaker_name           # variable for caretaker name
                last_update = fdb.time_since_last_update()  # variable for time of last update
                SMS = fdb.sms
                self.notify_and_update(f, fdb, project_name, caretaker_name, last_update, SMS)

        return 

    def notify_and_update(self, freedge, fdb, project_name, caretaker_name, last_update, SMS):
        '''
       Purpose: 
            TO BE IMPLEMENTED IF USING SMS NOTIFICATIONS
            Calls the notification interface class which will return a boolean value based on whether or not the
            Freedge is active from user input.
            Based on this boolean value, updates the freedge object status and then updates the freedge database status
            for the specific fridge object.

        Parameters: 
            caretaker_name -> str
            project_name -> str
            last_update -> int?

        Calls:
            update_status() of Freedge class

        Returns: None
        
        '''
        pass
        
