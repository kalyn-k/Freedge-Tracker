"""
===============================================================================
Title:	Notification GUI
===============================================================================
Description:	TODO: check--> The NotificationGUI is a prototype popup display of what a notification 
                from Freedge will look like. Because of money constraints, we were unable
                to purchase a Twilio Subscription to send real notifications. When signaled
                in NotificationMgmt, the notificationGUI will pop up with a message asking
                a caretaker if their fridge is still active. The Caretaker (or in this case,
                the user demonstrating the prototype) will select "YES" or "NO" and then 
                send the reply back to the main system in order to update the database of 
                current active fridges.

Authors: 		Kalyn Koyanagi, Ellie Kobak, Madison Werries
Last Edited: 	3-04-2022
Last Edit By:	Ellie Kobak

Edit Log
date         editor     changes
3-01-22      kek        created first working version
3-01-22      erk        documentation
3-02-22      kek        more documentation
3-03-22      mgw        edited popups so all text is visible and the popups
                        display one at a time, waiting for a response from
                        the user before proceeding.
3-04-22     erk         Updated documentation
"""

from tkinter import *                               # used to 
from freedge_database.freedge_data_entry import *   # used to access fridge object for data information

class PopUp:
    """
    # TODO is this okay?     <---- add description about the fact that this is for the prototype only.
    This class creates a pop-up window upon each class instantiation to send a notification
    to freedge caretakers. The class determines whether or not a freedge is still active
    as a result of the pop-up window options. This class is for the prototype only and serves to 
    demonstrate how a notification will be sent out, recieved, and interpreted by the system.
    """
    def __init__(self, root, freedge: Freedge):
        """
        TODO every variable in this function needs a comment explaining what it does!! TODO
        
        TODO:
        Purpose:

        Parameters:
            freedge: Freedge
        Called by: notify_and_update() in notificationMgmt.py to signal notification
        Returns: None, stores class information
        """
        self.root = root                                                # TODO
        self.response_received = BooleanVar()                           # TODO
        self.response_value = None                                      # TODO
        
        self.pop_up_win = Toplevel(self.root)                           # TODO
        self.pop_up_win.geometry("600x400")                             # TODO
        self.pop_up_win.resizable(False, False)                         # TODO
        self.pop_up_win.attributes("-topmost", True)                    # TODO
        self.pop_up_win.protocol("WM_DELETE_WINDOW", self.on_close)     # TODO
        self.pop_up_win.title("Simulated Status Check")                 # TODO change this?
        var = IntVar()                                                  # TODO

        ct_name = freedge.caretaker_name                                # TODO
        proj_name = freedge.project_name                                # TODO
        prev_update = freedge.last_status_update                        # TODO
        
        # Create a Header for the menu
        note = "This is a simulated text/email message for the Freedge Tracker System.\n"       # TODO
        header1 = Label(self.pop_up_win, width=200, text=note, fg="red", font=("TkDefaultFont", 10), wraplength=500) # Sets size of Header1
        header1.pack(padx=10, pady=15)  # TODO
        # Message to be displayed to caretaker
        self.message = f'Hi {ct_name}!\n' \
                       f'This is a message from the folks at freedge.org.\n\n' \
                       f'According to our systems, the status of your community fridge, "{proj_name}" in ' \
                       f'{freedge.fridge_location.ShortString()}, was last updated on: {prev_update}.\n\n' \
                       f' To keep our Freedge communities up-to-date, we would like to check in about the' \
                       f' status of this fridge. Please select one of the status options below, and click' \
                       f' "Send Reply" to confirm.\n\n\n'
        
        # Adds message for the notification
        header = Label(self.pop_up_win, width=200, text=self.message, fg="black",
                       font=("TkDefaultFont", 11), wraplength=500, justify=LEFT)
        header.pack(padx=10)        # TODO
        
        not_active = Radiobutton(self.pop_up_win, text="No longer active", variable=var, value=1,
                                 command=self.false_button)  # TODO
        active = Radiobutton(self.pop_up_win, text="Still active", variable=var, value=2, command=self.true_button) # TODO
        send_reply = Button(self.pop_up_win, text="Send Reply", command=self.exit_) # TODO
        not_active.pack()   # TODO
        active.pack()       # TODO
        send_reply.pack()   # TODO

    def false_button(self):
        """
        TODO:
        Purpose: Method to set the value of the status to false. Is called when
        the user selects the corresponding "No longer active" option button.

        Parameters: None
        Called by: get_status()
        Returns: False -> boolean value
        """
        self.response_value = Status.ConfirmedInactive     # set the user selected button to ConfirmedInactive

    def true_button(self):
        """
        Purpose: Method to set the value of the status
        to True. Is called when the user selects the
        corresponding "Still active"
        option button.

        Parameters: None
        Called by: get_status()
        Returns: True -> boolean value
        """
        self.response_value = Status.Active     # set the user selected button to Active

    def get_response(self):
        """
        TODO
        Purpose: Method to return the status of a notification
        sent to the user.
        Parameters: None

        Called by: notify_and_update() in notificationMgmt.py to update fridge activity in database
        Returns: boolean value
        """
        return self.response_value              # return which button the user selected
    
    def on_close(self):
        """ 
        Purpose: If the user simply closes the window, record it as a non-response. This is akin to someone ignoring
        a message for an extended period of time.

        Parameter: None
        Called by: None
        Returns: None
        """
        self.response_value = None          # Initializes a response value
        self.response_received.set(True)    # Indicates response has been recorded
        self.pop_up_win.destroy()           # Closes popup window

    def exit_(self):
        """
        Purpose: Method to exit and end the program. Is called
        when user clicks corresponding exit
        button on the menu window.

        Parameter: None
        Called by: None
        Returns: None
        """
        self.response_value = self.get_response()   # Initializes a response value
        self.response_received.set(True)            # Indicates the response has been received successfully
        self.pop_up_win.destroy()                   # close the pop-up window
