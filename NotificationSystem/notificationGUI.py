"""
===============================================================================
Title:	Notification GUI
===============================================================================
Description:	The NotificationGUI is a prototype popup display of what a notification
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
from FreedgeDatabase.freedge_data_entry import *   # used to access fridge object for data information

class PopUp:
    """
    This class serves as a stand-in for prototype of the Freedge Tracker System,
    and the notifications it may send to freedge caretakers. In the real
    implementation, this would be replaced by real SMS and email messages,
    controlled by the files notificationMgmtSMS.py and notificationMgmtEmail.py.
    
    This class creates a pop-up window upon each class instantiation to send a
    notification to freedge caretakers. The class determines whether or not a
    freedge is still active  as a result of the pop-up window options.
    Again, this class is for the prototype only and serves to demonstrate how
    a notification may be sent out, recieved, and interpreted by the system.
    """
    def __init__(self, root: Tk, freedge: Freedge):
        """
        Initializes a new PopUp class with 'root' as the tkinter root of the
        display, filling in the popup window with information contained in
        the passed-in Freedge variable.

        Parameters:
            freedge: Freedge
        Called by: notify_and_update() in notificationMgmt.py to run the
                   display of the prototype notification system
        Returns: None, stores class information
        """
        # The tkinter root of the display (type: Tk)
        self.root: Tk = root
        # Whether or not the user has responded to the popup window yet
        self.response_received = BooleanVar()
        # The value of the user's response, either True, False, or None
        self.response_value = None
        # Create the popup window using a 'TopLevel' tkinter widget so that
        # it sits on top of the main application properly
        self.pop_up_win = Toplevel(self.root)
        
        self.pop_up_win.geometry("600x400")                             # Set size of the popup window
        self.pop_up_win.resizable(False, False)                         # Don't let the user resize the window
        self.pop_up_win.attributes("-topmost", True)                    # Set the pop to be the topmost window
        self.pop_up_win.protocol("WM_DELETE_WINDOW", self.on_close)     # Delete the window object when it is closed
        self.pop_up_win.title("Simulated Status Check")                 # Set the title of the popup
        var = IntVar()                                                  # The value received from the clickable bubbles

        ct_name = freedge.caretaker_name                                # Get the freedge caretaker's name to display
        proj_name = freedge.project_name                                # Get the freedge project name for the display
        prev_update = freedge.last_status_update                        # Get the last status update of the freedge
        
        # Create a Header for the menu
        note = "This is a simulated text/email message for the Freedge Tracker System.\n"
        # Define the style of the header for the menu
        header1 = Label(self.pop_up_win, width=200, text=note, fg="red",
                        font=("TkDefaultFont", 10), wraplength=500)
        # Set the location of the header in relation to the other objects (tkinter 'pack')
        header1.pack(padx=10, pady=15)
        # Create the formatted message to be displayed to caretaker
        self.message = f'Hi {ct_name}!\n' \
                       f'This is a message from the folks at freedge.org.\n\n' \
                       f'According to our systems, the status of your community fridge, "{proj_name}" in ' \
                       f'{freedge.fridge_location.ShortString()}, was last updated on: {prev_update}.\n\n' \
                       f' To keep our Freedge communities up-to-date, we would like to check in about the' \
                       f' status of this fridge. Is this freede still active? Please select one of the status' \
                       f' options below, and click "Send Reply" to confirm.\n\n\n'
        
        # Add a label to the popup window with the formatted message for the caretaker's notification
        header = Label(self.pop_up_win, width=200, text=self.message, fg="black",
                       font=("TkDefaultFont", 11), wraplength=500, justify=LEFT)
        # Set the location of the header in relation to the other objects (tkinter 'pack')
        header.pack(padx=10)
        # Retrieve the response value by creating radiobuttons on the popup window
        # Create the 'not active' radio button to simulate an SMS/email response of 'NO'
        not_active = Radiobutton(self.pop_up_win, text="NO, No longer active", variable=var, value=1,
                                 command=self.false_button)
        # Create the 'still active' radio button to simulate an SMS/email response of 'YES'
        active = Radiobutton(self.pop_up_win, text="YES, Still active", variable=var, value=2, command=self.true_button)
        # Create the button for the user to send their reply to the system
        send_reply = Button(self.pop_up_win, text="Send Reply", command=self.exit_)
        
        # Set the location of the buttons in relation to the other objects
        # (this is accomplished using tkinter's 'pack' function)
        not_active.pack()
        active.pack()
        send_reply.pack()

    def false_button(self):
        """
        Purpose: Method to set the value of the status to false. Is called when
        the user selects the corresponding "No longer active" option button.

        Parameters: None
        Called by: get_status()
        Returns: False -> boolean value
        """
        # set the user selected button to ConfirmedInactive
        self.response_value = Status.ConfirmedInactive

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
        # set the user selected button to Active
        self.response_value = Status.Active

    def get_response(self):
        """
        Purpose: Method to return the status of a notification
        sent to the user.
        Parameters: None

        Called by: notify_and_update() in notificationMgmt.py to update fridge activity in database
        Returns: boolean value
        """
        # return which button the user selected
        return self.response_value
    
    def on_close(self):
        """ 
        Purpose: If the user simply closes the window, record it as a
        non-response. This is akin to someone ignoring an SMS or email
        message for an extended period of time.

        Returns: None
        """
        # Sets the value of the response to 'None', as the user simply force-
        # closed the popup window rather than sending a reply
        self.response_value = None
        # A response has been recorded and the wait_variable has changed
        self.response_received.set(True)
        # Destroy the pop-up window object, removing it from the display
        self.pop_up_win.destroy()

    def exit_(self):
        """
        Purpose: Method to exit and end the program.
        
        Is called  when user clicks corresponding exit button on the
        popup notification window.
        
        Returns: None
        """
        # Retrieve the currently selected bubble as the user closes the window
        self.response_value = self.get_response()
        # Indicates the response has now been received
        self.response_received.set(True)
        # Destroy the pop-up window object, removing it from the display
        self.pop_up_win.destroy()
