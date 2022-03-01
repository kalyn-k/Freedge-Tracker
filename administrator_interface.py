"""
===============================================================================
Title:	Administrator Interface for the Freedge Tracker System
===============================================================================
Description:	TODO
Authors:        Kalyn Koyanagi
Last Edited:    2-25-2022
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
        self.treev = None
        self.menu = None

    def NewDatabase(self, event=None):
        # Get path of CSV file
        file_path = filedialog.askopenfilename()
        # Get path of database
        database_path = database_constants.DATABASE_PATH
        new_database_from_csv(database_path, file_path)
        # Update the menu window
        self.UpdateDisplayData()

    def UpdateDatabase(self, event=None):
        # Get path of CSV file
        file_path = filedialog.askopenfilename()
        # Get path of database
        database_path = database_constants.DATABASE_PATH
        new_database_from_csv(database_path, file_path)
        # Update the menu window
        self.UpdateDisplayData()

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

    def UpdateDisplayData(self):
        # Get list of list of freedges. freedges is a list of Freedge instances.
        # type(fdb) = FreedgeDatabase
        db_path = database_constants.DATABASE_PATH
        fdb = load_internal_database(db_path)
        freedges = fdb.get_freedges()
        num_db = len(freedges)
        # clear the treeview
        for item in self.treev.get_children():
            self.treev.delete(item)

        for fridge in range(num_db):
            self.treev.insert(parent='', index=fridge, iid=fridge, text='', values=(
                freedges[fridge].project_name, freedges[fridge].fridge_location.ToString(),
                freedges[fridge].caretaker_name,
                freedges[fridge].freedge_status.value, freedges[fridge].preferred_contact_method))

        self.treev.place(x=340, y=70)

    def OutOfDateOnly(self):
        # Replace the list of only out of date freedges
        db_path = database_constants.DATABASE_PATH
        fdb = load_internal_database(db_path)
        out_of_date = fdb.get_out_of_date()
        length_ood = len(out_of_date)

        for item in self.treev.get_children():
            self.treev.delete(item)

        for fridge in range(length_ood):
            self.treev.insert(parent='', index=fridge, iid=fridge, text='', values=(
                out_of_date[fridge].project_name, out_of_date[fridge].fridge_location.ToString(),
                out_of_date[fridge].caretaker_name,
                out_of_date[fridge].freedge_status.value, out_of_date[fridge].preferred_contact_method))

        self.treev.place(x=340, y=70)

    def MenuDisplay(self):
        # initiate the menu window, and set it's title
        self.menu = Tk()
        menu = self.menu
        menu.title("Freedge Tracker")  # TODO do we wanna change the title?
        # Sets window size
        menu.geometry("970x500")
        # Prevent the menu window from being resized
        menu.resizable(False, False)
        # Set menu background color
        menu.configure(bg='black')

        # Create a Header for the menu
        header = Label(menu, width=50, text="Freedge Tracker", bg="black", fg="white",
                       font=("TkDefaultFont", 22))
        header.pack(side=TOP, padx=10, pady=15)

        # Button to Create new database (db)
        create_db_button = Button(menu, text="Create new Database", font=("TkDefaultFont", 20),
                                  command=self.NewDatabase,
                                  bg="white", width=20)  # initiate the button
        create_db_button.place(x=45, y=70)

        # Button to update database
        update_db_button = Button(menu, text="Update Database", font=("TkDefaultFont", 20), command=self.UpdateDatabase,
                                  bg="white", width=20)  # initiate the button
        update_db_button.place(x=45, y=120)

        # Button to exit session
        exit_button = Button(menu, text="            Exit           ", font=("TkDefaultFont", 20), command=self.exit_,
                             bg="white", width=20)  # initiate the button
        exit_button.place(x=45, y=170)

        # Button to view only out of date freedges

        out_of_date_button = Button(menu, text="View only out of date freedges", font=("TkDefaultFont", 15),
                                    command=self.OutOfDateOnly, bg="white", width=20)
        out_of_date_button.place(x=45, y=220)

        self.treev = ttk.Treeview(menu, height=20)

        self.treev['columns'] = ('Project Name', 'Location', 'Owner', 'Status', 'Primary Contact')
        self.treev.column('#0', width=0, stretch=NO)
        self.treev.column('Project Name', anchor=CENTER, width=150)
        self.treev.column('Owner', anchor=CENTER, width=100)
        self.treev.column('Location', anchor=CENTER, width=120)
        self.treev.column('Status', anchor=CENTER, width=110)
        self.treev.column('Primary Contact', anchor=CENTER, width=110)
        self.treev.heading('#0', text='', anchor=CENTER)
        self.treev.heading('Project Name', text='Project Name', anchor=CENTER)
        self.treev.heading('Location', text='Location', anchor=CENTER)
        self.treev.heading('Owner', text='Owner', anchor=CENTER)
        self.treev.heading('Status', text='Status', anchor=CENTER)
        self.treev.heading('Primary Contact', text='Primary Contact', anchor=CENTER)

        self.treev.place(x=340, y=70)

        menu.mainloop()


if __name__ == '__main__':
    screen = admin_interface()
    screen.MenuDisplay()
