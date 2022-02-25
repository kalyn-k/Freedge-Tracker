"""
===============================================================================
Title:	Administrator Interface for the Freedge Tracker System
===============================================================================
Description:	TODO
Authors:        Kalyn Koyanagi
Last Edited:    2-23-2022
Last Edit By:   Kalyn Koyanagi
"""
import sys
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from freedge_internal_database import database_constants
from freedge_database import *


class admin_interface:
    def __init__(self):
        """
        TODO
        """
        # Define user windows for later use
        self.menu = None

    def NewDatabase(self, event=None):
        file_path = filedialog.askopenfilename()
        database_path = database_constants.DATABASE_PATH
        new_database_from_csv(database_path, file_path)

    def UpdateDatabase(self, event=None):
        file_path = filedialog.askopenfilename()
        database_path = database_constants.DATABASE_PATH
        new_database_from_csv(database_path, file_path)

    def CreateGraph(self):
        # call build_freedge_graph.py here
        pass

    def exit_(self):
        """
        Method to exit and end the program. Is called
        when user clicks corresponding exit
        button on the menu window.

        Parameter:
            None
        Returns:
            None
        """
        sys.exit()  # use the exit method from the sys module

    def MenuDisplay(self):
        # initiate the menu window, and set it's title
        self.menu = Tk()
        menu = self.menu
        menu.title("Freedge Tracker")  # TODO do we wanna change the title?
        # Sets window size
        menu.geometry("850x650")
        # Prevent the menu window from being resized
        menu.resizable(False, False)
        # Set menu background color
        menu.configure(bg='black')

        # Button to Create new database (db)
        create_db_button = Button(menu, text="Create new Database", font=("TkDefaultFont", 20),
                                  command=self.NewDatabase,
                                  bg="white", width=20)  # initiate the button
        create_db_button.pack(padx=10, pady=10)

        # Button to update database
        update_db_button = Button(menu, text="Update Database", font=("TkDefaultFont", 20), command=self.UpdateDatabase,
                                  bg="white", width=20)  # initiate the button
        update_db_button.pack(padx=10, pady=10)

        # Button to exit session
        exit_button = Button(menu, text="            Exit           ", font=("TkDefaultFont", 20), command=self.exit_,
                             bg="white", width=20)  # initiate the button
        exit_button.pack(padx=10, pady=10)

        # TODO: the buttons to be added: Create Graph (?), ...
        # Get list of list of freedges. freedges is a list of Freedge instances.

        # TODO: Below is creating the scrollable frame

        treev = ttk.Treeview(menu)
        treev['columns'] = ('Project Name', 'Location', 'Owner', 'Status', 'Primary Contact')
        treev.column('#0', width=0, stretch=NO)
        treev.column('Project Name', anchor=CENTER, width=80)
        treev.column('Owner', anchor=CENTER, width=80)
        treev.column('Location', anchor=CENTER, width=80)
        treev.column('Status', anchor=CENTER, width=80)
        treev.column('Primary Contact', anchor=CENTER, width=80)
        treev.heading('#0', text='', anchor=CENTER)
        treev.heading('Project Name', text='Project Name', anchor=CENTER)
        treev.heading('Location', text='Location', anchor=CENTER)
        treev.heading('Owner', text='Owner', anchor=CENTER)
        treev.heading('Status', text='Status', anchor=CENTER)
        treev.heading('Primary Contact', text='Primary Contact', anchor=CENTER)

        treev.insert(parent='', index=0, iid=0, text='', values=('Freedge@UO', 'Eugene', 'Ernst', 'Active', 'ernst@freedge.com'))
        treev.pack()
        menu.mainloop()

if __name__ == '__main__':
    screen = admin_interface()
    screen.MenuDisplay()
