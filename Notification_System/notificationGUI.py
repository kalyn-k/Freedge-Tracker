"""
===============================================================================
Title:	Notification GUI
===============================================================================
Description:	TODO

Authors: 		Kalyn Koyanagi, Ellie Kobak, Madison Werries
Last Edited: 	3-03-2022
Last Edit By:	Madison Werries

Edit Log
date         editor     changes
3-01-22      kek        created first working version
3-01-22      erk        documentation
3-02-22      kek        more documentation
3-03-22      mgw        edited popups so all text is visible and the popups
                        display one at a time, waiting for a response from
                        the user before proceeding.
"""

from tkinter import *
from Freedge_Database.freedge_data_entry import *   # used to access fridge object for data information

class PopUp:
    """
    # TODO is this okay?     <---- add description about the fact that this is for the prototype only.
    This class creates a pop-up window upon each class instantiation to send a notification
    to freedge caretakers. The class determines whether or not a freedge is still active
    as a result of the pop-up window options.
    """
    def __init__(self, root, freedge: Freedge):
        """
        TODO:
        Purpose:

        Parameters:
            freedge: Freedge
        Called by: notify_and_update() in notificationMgmt.py to signal notification
        Returns: None, stores class information
        """
        self.root = root
        self.response_received = BooleanVar()
        self.response_value = None
        
        self.pop_up_win = Toplevel(self.root)
        self.pop_up_win.geometry("600x400")
        self.pop_up_win.resizable(False, False)
        self.pop_up_win.attributes("-topmost", True)
        self.pop_up_win.protocol("WM_DELETE_WINDOW", self.on_close)
        self.pop_up_win.title("Simulated Status Check")  # TODO change this?
        var = IntVar()

        ct_name = freedge.caretaker_name
        proj_name = freedge.project_name
        prev_update = freedge.last_status_update
        
        # Create a Header for the menu
        note = "This is a simulated text/email message for the Freedge Tracker System.\n"
        header1 = Label(self.pop_up_win, width=200, text=note, fg="red", font=("TkDefaultFont", 10), wraplength=500)
        header1.pack(padx=10, pady=15)
        self.message = f'Hi {ct_name}!\n' \
                       f'This is a message from the folks at freedge.org.\n\n' \
                       f'According to our systems, the status of your community fridge, "{proj_name}" in ' \
                       f'{freedge.fridge_location.ShortString()}, was last updated on: {prev_update}.\n\n' \
                       f' To keep our Freedge communities up-to-date, we would like to check in about the' \
                       f' status of this fridge. Please select one of the status options below, and click' \
                       f' "Send Reply" to confirm.\n\n\n'
        
        # Add the message for the notification
        header = Label(self.pop_up_win, width=200, text=self.message, fg="black",
                       font=("TkDefaultFont", 11), wraplength=500, justify=LEFT)
        header.pack(padx=10)
        
        not_active = Radiobutton(self.pop_up_win, text="No longer active", variable=var, value=1,
                                 command=self.false_button)
        active = Radiobutton(self.pop_up_win, text="Still active", variable=var, value=2, command=self.true_button)
        send_reply = Button(self.pop_up_win, text="Send Reply", command=self.exit_)
        not_active.pack()
        active.pack()
        send_reply.pack()

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
        """ If the user simply closes the window, record it as a non-response. This is akin to someone ignoring
            a message for an extended period of time.
        """
        self.response_value = None
        self.response_received.set(True)
        self.pop_up_win.destroy()

    def exit_(self):
        """
        Purpose: Method to exit and end the program. Is called
        when user clicks corresponding exit
        button on the menu window.

        Parameter: None
        Called by: None
        Returns: None
        """
        self.response_value = self.get_response()
        self.response_received.set(True)
        self.pop_up_win.destroy()               # close the pop-up window
