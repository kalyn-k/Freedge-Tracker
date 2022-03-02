"""
===============================================================================
Title:	Administrator Interface for the Freedge Tracker System
===============================================================================
Description:	TODO
Authors:        Kalyn Koyanagi, Madison Werries
Last Edited:    2-28-2022
Last Edit By:   Madison Werries
"""
import sys
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkinter.ttk import Notebook
from freedge_internal_database import database_constants
from freedge_database import *
from freedge_data_entry import *

# TODO: =======================================================================
# Update database
# Not supposed to be notified, but is out-of-date
# rename update_date

class admin_interface:
    def __init__(self):
        """
        TODO
        """
        # Define user windows for later use
        self.fdb = None         # Connection to Freedge database
        self.main_tab = None    # All freedges tab
        self.ood_tab = None     # Out of date freedges tab
        self.menu = None
        
    def LoadDatabase(self):
        # Load the internal database
        self.fdb = load_internal_database(DATABASE_PATH)
        # Update the display tables
        self.UpdateFullDisplay()

    def NewDatabase(self):
        # Get the path of CSV file from the user
        messagebox.askokcancel("File select", "Select a csv file to load into the database.")
        file_types = [('csv files', '.csv')]
        file_path = filedialog.askopenfilename(title="Please select the csv file containing the freedge data.",
                                               filetypes=file_types)
        if (file_path == ""):
            answer = messagebox.askretrycancel("Question", "Error: No file selected. Please hit 'Retry'"
                                                           " to select a csv file, or 'Cancel' to close the program.")
            # If the user hit 'Cancel' or 'X', exit the application
            if (not answer):
                self.exit_()
            # If the user hit 'Retry', try to prompt them again to load a new database
            else:
                self.NewDatabase()
        # Create a new database using the data from the CSV file
        self.fdb = new_database_from_csv(DATABASE_PATH, file_path)
        # Update the display
        self.UpdateFullDisplay()

    def UpdateDatabase(self, event=None):
        # TODO: output what will be changed
        # Get path of CSV file
        file_path = filedialog.askopenfilename()
        (to_add, to_remove, to_modify) = self.fdb.compare_databases(file_path)
        message = "If you load the selected csv file into the database, the following changes will be made:\n"
        message += "-----------------------------------------------------------\n"
        if (len(to_add) > 0):
            message += "Freedges which will be ADDED:"
            for freedge in to_add:
                message += "\t" + freedge.ToString() + "\n"
            message += "-----------------------------------------------------------\n"
        if (len(to_remove) > 0):
            message += "Freedges which will be REMOVED:"
            for freedge in to_remove:
                message += "\t" + freedge.ToString() + "\n"
            

        if (len(to_modify) > 0):
            message += "Freedges whose data will be MODIFIED:"
            for (f1, f2) in to_modify:
                changes = f1.compare_freedges(f2)
                message += "\t" + f1.ToString() + "\n"
                for change in changes:
                    message += change
        messagebox.askokcancel("Proceed?", message+" Is this ok?")
        # Get path of database
        self.fdb = new_database_from_csv(DATABASE_PATH, file_path)
        # Update the menu window
        self.UpdateFullDisplay()

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

    def UpdateFullDisplay(self):
        freedges = self.fdb.get_freedges()
        out_of_date = self.fdb.get_out_of_date()
        screen.UpdateTableDisplay(self.main_tab, freedges)
        screen.UpdateTableDisplay(self.ood_tab, out_of_date)
    
    def UpdateTableDisplay(self, table, freedges: [Freedge]):
        # clear the list of freedges
        for item in table.get_children():
            table.delete(item)
            
        # Add the new list of freedges
        for fridge in range(len(freedges)):
            if (fridge % 2 == 0):
                tag = "even_row"
            else:
                tag = "odd_row"
            f = freedges[fridge]
            contact = "-"
            if (f.preferred_contact_method == ContactMethod.SMS.value):
                contact = f.phone_number
            if (f.preferred_contact_method == ContactMethod.Email.value):
                contact = f.email_address
            table.insert(parent='', index=fridge, iid=fridge, text='', tags=tag, values=(
                f.project_name, f.fridge_location.ToString(),
                f.caretaker_name, f.freedge_status.value, f.last_status_update,
                f.time_since_last_update(), f.permission_to_notify, contact))

    def BuildTable(self, tab):
        # Structure the table view of the Freedges
        columns = ('Project Name', 'Location', 'Owner', 'Freedge Status',
                   'Last Status Update', 'Time Since Last Update', 'Permission to Notify?', 'Primary Contact')
        table = ttk.Treeview(tab, height=20, columns=columns, show='headings', selectmode='browse')
        table.place(x=0, y=0)
    
        # Insert the columns
        table.column('#0', width=0, stretch=NO)
        table.column('Project Name', anchor=CENTER, width=200)
        table.column('Location', anchor=CENTER, width=100)
        table.column('Owner', anchor=CENTER)
        table.column('Freedge Status', anchor=CENTER, width=150)
        table.column('Last Status Update', anchor=CENTER, width=100)
        table.column('Time Since Last Update', anchor=CENTER, width=200)
        table.column('Permission to Notify?', anchor=CENTER, width=100)
        table.column('Primary Contact', anchor=CENTER, width=200)
    
        # Insert the headers
        table.heading('#0', text='')
        table.heading('Project Name', text='Project Name')
        table.heading('Location', text='Location')
        table.heading('Owner', text='Owner')
        table.heading('Freedge Status', text='Freedge Status')
        table.heading('Last Status Update', text='Last Update')
        table.heading('Time Since Last Update', text='Time Since Last Update')
        table.heading('Permission to Notify?', text='Can Notify?')
        table.heading('Primary Contact', text='Primary Contact')
        table.tag_configure("odd_row", background="white")

        return table

    def MenuDisplay(self):
        # Initialize the display for the Administrator Interface
        root = Tk()
        root.title("Freedge Tracker")
        width = root.winfo_screenwidth()-100
        height = root.winfo_screenheight()-150
        root.geometry("%dx%d" % (width, height))
        root.wm_state('zoomed')
        root.configure(bg='gray')      # Set menu background color
        root.maxsize()
        self.menu = root

        # Create a Header for the menu
        header = Label(root, width=50, text="Freedge Tracker", bg="gray", fg="white",
                       font=("TkDefaultFont", 30))
        header.pack(side=TOP, padx=10, pady=30)

        # =====================================================================
        # Creating the Freedge Info Tables
        # =====================================================================
        # Tabs for the table (https://www.geeksforgeeks.org/creating-tabbed-widget-with-python-tkinter/)
        notebook = Notebook(root)
        tab1 = Frame(notebook, width=width-200, height=500)
        tab2 = Frame(notebook, width=width-200, height=500)
        notebook.add(tab1, text='    All    ')
        notebook.add(tab2, text='Out of Date')
        notebook.place(x=250, y=100)

        # Build the tables to be displayed in the two tabs
        self.main_tab = self.BuildTable(tab1)
        self.ood_tab = self.BuildTable(tab2)
    
        # =====================================================================
        # Creating the GUI Buttons
        # =====================================================================
        # Button to Create new database (db)
        create_db_button = Button(root, text="Create new Database", font=("TkDefaultFont", 12),
                                  command=self.NewDatabase,
                                  bg="white", width=20)  # initiate the button
        create_db_button.place(x=45, y=150)

        # Button to update database
        update_db_button = Button(root, text="Update Database", font=("TkDefaultFont", 12), command=self.UpdateDatabase,
                                  bg="white", width=20)  # initiate the button
        update_db_button.place(x=45, y=200)

        # Button to exit session
        exit_button = Button(root, text="            Exit           ", font=("TkDefaultFont", 12), command=self.exit_,
                             bg="white", width=20)  # initiate the button
        exit_button.place(x=45, y=250)
        
        # =====================================================================
        # Configure the style of the display
        # =====================================================================
        # Notebook color
        bg_color = "lightgrey"
        gold_color = "gold"
        color_tab = "#ccdee0"
        
        # style
        style = ttk.Style()
        default_font = 'Helvetica'
        
        style.theme_create("freedge_theme", parent="default", settings={
            "TNotebook": {
                "configure": {"tabmargins": [10, 10, 20, 10], "background": bg_color}},
            "TNotebook.Tab": {
                "configure": {"padding": [30, 10], "background": bg_color, "font": (default_font, 14),
                              "borderwidth": [0]},
                "map": {"background": [("selected", gold_color), ('!active', bg_color), ('active', color_tab)],
                        "expand": [("selected", [1, 1, 1, 0])]}},
            "TFrame": {
                "configure": {"background": "black"}},
            "Treeview.Heading": {
                "configure": {"font": (default_font, 12), "foreground": "orange", "background": "dimgray"}},
            'Treeview': {
                'map': {
                    'background': [('!selected', 'lightgrey'), ('selected', 'white')],
                    'font': [('selected', ("Century Gothic", 10, 'bold'))],
                }
            },
            ".": {
                "configure": {"font": (default_font, 10), "foreground": "gray"}
            }
        })
        style.theme_use("freedge_theme")
        if (exists_internal_database(DATABASE_PATH)):
            title = "An existing database was found at: " + DATABASE_PATH +\
                    ".\n\nWould you like to proceed with that database? Hit 'yes' to continue," \
                    "'no' to select a different database, or 'cancel' to quit."
            
            response = messagebox.askyesnocancel("Database Found", title)
            if (response is None):
                self.exit_()
            elif (not response):
                self.NewDatabase()
            else:
                screen.LoadDatabase()
                screen.UpdateFullDisplay()
        root.mainloop()


if __name__ == '__main__':
    screen = admin_interface()
    screen.MenuDisplay()

