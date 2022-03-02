"""
===============================================================================
Title:	Notification GUI
===============================================================================
Description:	TODO

Authors: 		Kalyn Koyanagi, Ellie Kobak
Last Edited: 	3-01-2022
Last Edit By:	Ellie Kobak

Edit Log
date         editor     changes
3-01-22      kk         created first working version 
3-01-22      erk        documentation

"""
from tkinter import * 

# TODO
# Test values
caretaker_name = "Liza"
project_name = "Sample Fridge"
last_update = "02-28-2022"
message = f'Hello {caretaker_name}, {project_name} was last determined as active on {last_update}. Is this fridge ' \
          f'still active? Please reply YES or NO '


class Pop_up:
    '''
    TODO: description of class
    '''
    def __init__(self, caretaker_name, project_name, last_update):
        '''
        TODO:
        Purpose:

        Parameters:
            caretaker_name -> str
            project_name -> str
            last_update -> int?

        Called by: notify_and_update() in notificationMgmt.py to signal notification

        Returns: None, stores class information

        '''
        self.selected_button = False
        self.ct_name = caretaker_name
        self.proj_name = project_name
        self.latest_update = last_update
        self.message = f'Hello {self.ct_name}, {self.proj_name} was last determined as active \non {self.latest_update}' \
                       f'. Is this fridge still active? Please select one of the\n status options below and then click ' \
                       f'on "Send Reply" '
        self.pop_up_win = Tk()
        self.pop_up_win.geometry("600x200")
        self.pop_up_win.title("Status Check")  # TODO change this?
        var = IntVar()
        # Create a Header for the menu
        header = Label(self.pop_up_win, width=75, text=self.message, bg="white", fg="black",
                       font=("TkDefaultFont", 15))
        header.pack(side=TOP, padx=10, pady=15)

        not_active = Radiobutton(self.pop_up_win, text="No longer active", variable=var, value=1,
                                 command=self.false_button)
        active = Radiobutton(self.pop_up_win, text="Still active", variable=var, value=2, command=self.true_button)
        send_reply = Button(self.pop_up_win, text="Send Reply", command=self.exit_)
        not_active.pack()
        active.pack()
        send_reply.pack()
        self.pop_up_win.mainloop()

    def false_button(self):
        '''
        TODO:
        Purpose:

        Parameters: None
            
        Called by: get_status()

        Returns: False -> boolean value
        '''
        self.selected_button = False

    def true_button(self):
        '''
        TODO:
        Purpose:

        Parameters: None
            
        Called by: get_status()

        Returns: True -> boolean value
        '''
        self.selected_button = True

    def get_status(self):
        '''
        TODO:
        Purpose:

        Parameters: None
            
        Called by: notify_and_update() in notificationMgmt.py to update fridge activity in database

        Returns: False -> boolean value
        '''
        return self.selected_button

    def exit_(self):
        """
        Method to exit and end the program. Is called
        when user clicks corresponding exit
        button on the menu window.

        Parameter: None
        Called by: None
        Returns: None
        """
        self.pop_up_win.destroy()


if __name__ == '__main__':
    test = pop_up(caretaker_name,project_name,last_update)
    s = test.get_status()
    print(s)
