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
3-04-22      erk        updated documentation and code to match updated NotificationMgmt Class
"""

import internal_data.database_constants  # used to access constants for fridge object
import database as FD                         # used to access the database which contains each Freedge object and all the information on each fridge
import notification_system as NS                      # for prototype only, used for popup display of notification
 

class sms_mgmt(NS.NotificationMgmt):
    '''
    This class enables SMS notifications from freedge organizers to the fridge caretakers.
    The classhas the attributes to send SMS using the Twilio SMS API
    '''

    def __init__(self, root):
        """
        This function is set up to be updated for non prototype version.

        Parameters:  None

        Purpose:  initialize email management system to enable email communication between freedge organizers  and caretaker

        Calls:  In funtioning version, will call freedge_data_entry.py in order to obtain correct contact 
                info for each fridge.
        Returns: None, stores sender and reciever information in class initiation.
        """
        self.root = root # TODO
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
           
        Returns: None

        '''
        # call to the other classes in order to use their methods
        fdb = FD.load_internal_database(internal_data.database_constants.DATABASE_PATH_INFO)  # freedge database class initialization

        fridge_list = fdb.get_out_of_date()  # variable to obtain the list of freedge objects that are out of date

        # Iterates through list of freedge objects and obtains the caretaker's name, project name, and time since
        # last update. These three items will be returned by the function to be used to craft a message to the
        # caretaker through the notification GUI.
        for fridge in fridge_list:
            if fridge.can_notify():
                return
            # signals the notifcation to be sent out

        return

    def notify_and_update(self, fdb, freedge):
        '''
       Purpose: 
            TO BE IMPLEMENTED IF USING SMS NOTIFICATIONS
            Calls the notification interface class which will return a boolean value based on whether or not the
            Freedge is active from user input.
            Based on this boolean value, updates the freedge object status and then updates the freedge database status
            for the specific fridge object.

        Parameters: 
            fdb -> fridge database object
            freedge -> freedge object

        Calls: notificationGUI.py in order to notify user of fridge activity
            update_status() of Freedge class

        Called by: get_fridge_info_message

        Returns: None
        
        '''
        pass
        
