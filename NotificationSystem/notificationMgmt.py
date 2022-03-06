"""
===============================================================================
Title:	notificationMgmt.py
===============================================================================
Description:	Obtains which freedges in the database are considered out of date and collects their associated
                data (caretaker name, project name, and time since last update) to be used when crafting a
                notification message by the notification GUI. Also uses the user response from the GUI to then
                update the status of the Freedge in the database.

Authors: 		Ellie Kobak, Liza Richards, Madison Werries
Creation Date:  February 17, 2022
Last Edited: 	3-04-2022
Last Edit By:	Ellie Kobak


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
3-02-22     erk         documentation
3-03-22     mgw         changed the way the NotificationMgmt class is initialized so the notifications are properly
                        integrated with the Administrator Interface (administrator_interface.py)
3-04-22     erk         updated documentation to make more consistent
3-06-22     mgw         finalized documentation; filled in all docstring TODOs
"""
import InternalData.freedge_constants  # used to access constants for fridge object
import FreedgeDatabase as FD                         # used to access the database which contains each Freedge object and all the information on each fridge
import NotificationSystem as NS                      # for prototype only, used for popup display of notification

class NotificationMgmt():
    """
    This class is the parent class for all notification systems. The class is designed using modularity
    so every class that inherits NotificationMgmt can add additional methods specific for the notification
    system. The class has the attributes to signal a popup notification.
    """
    def __init__(self, root):
        """
        Purpose:
            Creates a new instance of the NotificationMgmt class, setting the root tkinter display
        Parameters:
            root: TK, the tkinter root for the GUI display, passed in from the main driver.

        Returns: None, initializes NotififacationMgmt class
        """
        self.root = root
        
    def get_fridge_info_message(self):
        """
        Purpose:
            This function obtains which freedges are out of date (have not had a status update in 90 days),
            collects the freedge's caretaker, name, and time since last update to be used to craft a message for the
            notification GUI. The function also update the freedge object's status based on user response, and then
            further update the freedge database.

        Parameters: None
       
        Calls:
            called by: admin_interface.py when system has not been notified of activity in 90 days, or if
                    user presses the notify button
                    notify_and_update() to send notification
        Returns: None
        """
        # call to the other classes in order to use their methods
        # freedge database class initialization
        fdb = FD.load_internal_database(InternalData.freedge_constants.DATABASE_PATH_INFO)

        fridge_list = fdb.get_out_of_date()  # variable to obtain the list of freedge objects that are out of date

        # Iterates through list of freedge objects and obtains the caretaker's name, project name, and time since
        # last update. These three items will be returned by the function to be used to craft a message to the
        # caretaker through the notification GUI.
        for fridge in fridge_list:
            if fridge.can_notify():
                return
            # signals the notifcation to be sent out
                # self.notify_and_update(fdb, fridge)

        return

    def notify_and_update(self, fdb, freedge):
        """
        Purpose:
            Calls the  interface class which will return a boolean
            value based on whether or not the Freedge is active from user input.
            Based on this boolean value, updates the freedge object status and
            then updates the freedge database status for the specific Freedge
            using the freedge_id to look up the entry in the database.

        Parameters: 
            fdb -> FreedgeDatabase object to interact with the SQLite database
            freedge -> Freedge object to be updated

        Calls: notificationGUI.py in order to notify user of fridge activity
            update_status() of Freedge class

        Called by: get_fridge_info_message

        Returns: None
        """
        # calls notification GUI pop up function to send message
        popup = NS.notificationGUI.PopUp(self.root, freedge)
        
        # Using a tkinter 'wait_variable' allows us to temporarily pause the
        # program before proceeding. A 'wait_variable' acts as a brief lock,
        # requesting that the system wait until the value of the passed-in
        # variable changes before proceeding.
        popup.pop_up_win.wait_variable(popup.response_received)
        # Retrieve the response of the user
        response = popup.get_response()
        
        # If the user did not respond:
        if response is None:
            print("no response.")
        # If the user did respond
        else:
            # Update the status of the Freedge according to the user's response
            freedge.update_status(response)
            # Reset the last update of the Freedge (sets to today's date)
            freedge.reset_last_update()
            # update the SQLite freedge database with the updated information
            fdb.update_freedge(freedge)
        return




