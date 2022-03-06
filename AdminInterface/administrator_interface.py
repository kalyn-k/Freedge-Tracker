"""
===============================================================================
Title:	Administrator Interface for the Freedge Tracker System
===============================================================================
Description:	This is the Administrator Interface module for the Freedge
                Tracker System. It is the main driver for the system, and
                is responsible for both I/O from an administrator and the
                GUI display to the admin (the user).
                
Authors:        Kalyn Koyanagi, Madison Werries
Last Edited:    3-5-2022
Last Edit By:   Madison Werries

Resources/help in using tkinter found at:
    (1) The method for how to create tabbed windows was derived from:
        (https://www.geeksforgeeks.org/creating-tabbed-widget-with-python-tkinter/)
"""
from tkinter.ttk import *
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import NotificationSystem as NS
from FreedgeDatabase import *
from AdminInterface.tkinter_style import *
import sys

class AdministratorInterface:
    """
    The class responsible for the main interface of the Freedge Tracker System.
    It manages both the I/O and the GUI display to the Freedge Administrators.
    
    Attributes
    ===========================================================================
    fdb_path: str
        The full path to open the internal database file
        
    fdb: FreedgeDatabase
        This is instance of the FreedgeDatabase class which is currently open
        in the system, if any. The abbreviation stands for "Freedge database."
        
    root: Tk
        The root of the GUI display, created by calling Tk().
    
    notebook: Notebook
        The tkinter Notebook responsible for displaying the table of freedge
        database information. It contains two tabs: the main_tab, which shows
        the list of all the freedges, and the ood_tab, which shows the list of
        freedges with out of date information.

    main_tab
       The GUI for displaying the table list of all freedges in the database.
       A child of self.notebook.
       
    ood_tab
        The GUI for showing the table list of all freedges in the database
        which are considered to be "out-of-date".
        A child of self.notebook
    
    info_box
        GUI tkinter Frame for displaying information about a particular
        freedge, updated whenever the user clicks on an entry in the table.
    
    info_label
        The tkinter Label which controls the text of the currently selected
        freedge info. A child of info_box.
        
    ib_width
        Fixed width to maintain consistency for the info_box display Labels.
    
    prompt_label
        A tkinter Label which shows text instructions prompting the user for
        action. This is shown when no database has been loaded yet, and is
        destroyed after a database has been loaded into the system.
    
    Methods
    ===========================================================================
    __init__()
        Initializes a new instance of the AdminInterface class.
        Requires no arguments.
    
    CreateDatabase()
        Creates a new internal freedge database. Both the csv file to load and
        the location/name of the new db file to save to are chosen by the user
        via popup prompts. Calls SelectCSVFile(), SelectDBSave(), and
        OpenDatabase().
    
    LoadDatabase(db_file_path)
        Opens the database at the given path, loading the database into the
        system and updating the internal file which stores the most recently
        accessed databse file. Called by SelecteDatabaseToLoad() and the
        main driver module, freedge_tracker.py.
    
    SelectCSV()
        Prompts the user to choose a csv file to load during the creation of a
        new database. Returns the chosen path if one is selected successfully,
        or None otherwise. Called by CreateDatabase().
        
    SelectDBSave()
        Prompts the user to choose the name and location of the db file to
        save their newly created database to. Returns the chosen path if one
        is selected successfully, or None otherwise. Called by CreateDatabase().
    
    SelectAndOpenDB()
        Prompts the user to choose a preexisting SQL database file (.db) to
        load into the system, updating the display with the information in
        the chosen db file. Calls LoadDatabase() and UpdateFullDisplay().
        Called by pressing the tkinter button labeled 'Load Database'.
    
    UpdateDatabase()
        Updates the currently loaded database file (db) with information from
        a new csv file that the user selects. Informaton about freedges which
        will be added to, removed from, and modified within the database is
        displayed to the user, allowing them to confirm or cancel the update.
    
    GetSelected()
        Returns the Freedge object corresponding to the user's currently
        selected entry in the display table, if any. If nothing is selected,
        the function returns None.
        
    OnTableClick()
        Called when the user clicks on an entry in the GUI table listing the
        freedge data entries. Calls GetSelected(), updating the info_box with
        the newly selected data, if any.
        
    NotifyFreedge(freedge)
        Sends a notification to the caretaker of the passed-in Freedge object.
    
    NotifySelected()
        Sends a notification to the caretaker of the freedge that is currently
        selected by the user in the display table, if any. Called when the user
        clicks on the GUI button 'Notify Selected'.
    
    NotifyOutOfDate()
        Sends a notification to each of the caretakers who have not been
        contacted in the amount of time defined by FIRST_UPDATE_THRESHOLD in
        the constants file (InternalData/database_constants.py). The system
        first prompts the user with information about the freedges which will
        be messaged, allowing them to confirm or cancel the mass-send.
    
    UpdateFullDisplay()
        Updates the GUI display to reflect the currently loaded database
        information. This is called on system startup, anytime a notification
        reply is received from a caretaker, as well as any time a new database
        is created/loaded.
        
    UpdateTableDisplay(table, freedges: [Freedge])
        Updates the information in a particular display table to contain the
        information stored in the array of Freedge objects passed in. This
        avoids duplicate code when updating the table tabs ('All', the main
        tab, and 'Out of Date', the tab showing only the out of date freedges).
        
    BuildTable(tab)
        Constructs the GUI elements necessary for a display table, using the
        passed-in tab argument as the parent object.
    
    AddButton(parent, label, cmd, xpos, ypos)
        Creates a new button on the GUI display. Sets the parent, the text
        label, the command (function) to call when pressing the button, and
        the position of the button based on the given parameters.
        
    CreateDisplay()
        Builds the full tkinter GUI display of the Administrator Interface.
        
    exit_
        Exits the program.
    """
    def __init__(self):
        """
        Initializes a new instance of the AdminInterface class.
        """
        self.fdb_path = None        # The file path to the internal database
        self.fdb = None             # The FreedgeDatabase object
        self.root = None            # The root of the GUI display
        self.main_tab = None        # Tab display showing all freedges
        self.ood_tab = None         # Tab for showing out-of-date freedges
        self.notebook = None        # The panel containing the two tabs
        self.info_box = None        # GUI for info about a particular freedge
        self.info_label = None      # Currently displayed freedge info
        self.prompt_label = None    # Text to prompt user for action (used
                                    # when no database has been loaded yet)
        self.ib_width = 30          # Fixed width for info_box display
    
    # =========================================================================
    # Database I/O Methods
    # =========================================================================
    
    def CreateDatabase(self):
        """
        Creates a new internal freedge database, updating the GUI if necessary.
        
        Returns: None
        """
        # Prompt the user to select the csv file to use to create the database
        csv_file_path = self.SelectCSV()
        if csv_file_path is None:           # Verify the user's response
            return
        # Prompt the user to select the name/location to store the database at
        db_file_path = self.SelectDBSave()
        if db_file_path is None:            # Verify the user's response
            return
        # If the above steps were successful, load the database into the system
        self.LoadDatabase(db_file_path)
        # Update the display to reflect the newly loaded database information
        self.UpdateFullDisplay()

    def LoadDatabase(self, db_file_path: str):
        """
        Loads the database at the given path into the system.
        
        Parameters:
            db_file_path:   The str path of the .db file to open

        Returns: None
        """
        # Verify that the path correctly specifies the location of a db file
        if not exists_internal_database(db_file_path):
            FileNotFoundError("Could not locate the database at: ", db_file_path)
        
        # Load the database file as an instance of the FreedgeDatabase class
        self.fdb = load_internal_database(db_file_path)
        # Update the interface's current database path for future use
        self.fdb_path = db_file_path
        # Save/update the path of the most recently accessed database using the
        # file whose path is specified at DATABASE_PATH_INFO
        saved_fdb_path = open(DATABASE_PATH_INFO, "w+")
        # Write the header for the internal path file
        saved_fdb_path.write("This is a text file which contains the file path to"
                             " the last database(.db file) that was opened.\n")
        # Write the actual file location, and close the file
        saved_fdb_path.write(self.fdb_path)
        saved_fdb_path.close()
    
    def SelectCSV(self):
        """
        Prompts the user to choose a csv file to load.
        
        Returns: The path as a str to the csv file the user selected, or None
                 if no path was selected.
        """
        # Define the info to show the user before showing the file-select
        prompt = "Please select the csv file containing the data you would" \
                 " like to use to create a new freedge database."
        
        # Before showing the file-select window, notify the user of the purpose
        # of the task (ie, why they're selecting a file)
        user_response = messagebox.showinfo("Please Select a CSV file", prompt)
        if user_response is None or not user_response:
            # If the user hit 'X' or 'Cancel', return None
            return None
        
        # Get the path of CSV file from the user using a tkinter filedialog box
        csv_file_path = filedialog.askopenfilename(
            title="Please select the csv file to load.",
            filetypes=[('csv files', '.csv')])

        # If they provided a filename correctly, return it.
        if (csv_file_path != "" and csv_file_path is not None):
            return csv_file_path
        # Otherwise, return None.
        return None

    def SelectDBSave(self):
        """
        Prompts the user to choose the name and location of the db file to
        save their newly created database to.
        
        Returns: The path as a str to the csv file the user selected, or None
                 if no path was selected.
        """
        # Before showing the file-select window, notify the user of the purpose
        # of the task (ie, why they're selecting a file)
        prompt = "Please provide the name/location of where you would like" \
            " to save the internal database file."
        messagebox.showinfo("Save internal database", prompt)
        
        # Get the path of db file from the user using a tkinter filedialog box
        db_file_path = filedialog.asksaveasfilename(
            title="Select location to store the internal database file",
            filetypes=[('SQL db files', '.db')], defaultextension=".db")
        # If they provided a filename correctly, return it.
        if (db_file_path != "" and db_file_path is not None):
            return db_file_path
        # Otherwise, return None.
        return None
    
    def SelectAndOpenDB(self):
        """
        Prompts the user to choose a preexisting SQL database file (.db) to
        load into the system, updating the display with the information in
        the chosen db file.
        
        Returns: None
        """
        file_types = [('db files', '.db')]
        prompt = "Please select the .db file to load into the system."
        # Briefly describe the task to the user before showing the file-select
        messagebox.showinfo("Select internal database location", prompt)
        # Ask the user to select a db file to load into the system
        db_file_path = filedialog.askopenfilename(
            title="Please select the internal database file.",
            filetypes=file_types, defaultextension=".db")
        # If they provided a filename correctly, return it. Otherwise, return None.
        if (db_file_path != ""):
            self.LoadDatabase(db_file_path)
        # Update the display tables
        self.UpdateFullDisplay()

    def UpdateDatabase(self):
        """
        Updates the currently loaded database file (db) with information from
        a new csv file that the user selects.
        
        Returns: None
        """
        # Get path of CSV file to load in in order to update the database
        file_path = filedialog.askopenfilename()
        (to_add, to_remove, to_modify) = self.fdb.compare_databases(file_path)
        if (len(to_add) == 0 and len(to_remove) == 0 and len(to_modify) == 0):
            message = "Loading the selected csv file will not change any data in the database."
        else:
            message = "If you load the selected csv file into the database, the following changes will be made:\n\n"
      
        if (len(to_add) > 0):
            message += "(" + str(len(to_add)) + ") entries will be ADDED.\n"
            # for freedge in to_add:
            # message += freedge.ToString() + "\n"
        if (len(to_remove) > 0):
            message += "(" + str(len(to_remove)) + ") entries will be REMOVED.\n"
            # message += "===== Freedges which will be REMOVED =====\n"
            # for freedge in to_remove:
            # message += freedge.ToString() + "\n"
        if (len(to_modify) > 0):
            message += "(" + str(len(to_modify)) + ") entries will be MODIFIED.\n"
            # message += "===== Freedges whose data will be MODIFIED =====\n"
            # for (f1, f2) in to_modify:
            # changes = f1.compare_freedges(f2)
            # message += f1.ToString() + "\n"
            # for change in changes:
            # message += change
        messagebox.askokcancel("Proceed?", message+" Proceed?")
        # Get path of database
        self.fdb = new_database_from_csv(self.fdb_path, file_path)
        # Update the menu window
        self.UpdateFullDisplay()

    # =========================================================================
    # GUI Methods Called Via User I/O
    # =========================================================================
        
    def GetSelected(self):
        """
        Gets the user's currently selected entry in the display table, if any.
        
        Returns: A Freedge object corresponding to the user's currently
                 selected entry in the table, or None if nothing is selected.
        """
        # If the database has not been loaded yet, return None
        if self.fdb is None:
            return None
        # Get the tkinter Notebook containing the data table display
        nb = self.notebook
        
        # Get the index of the notebook's active tab ('all' or 'out of date')
        i = self.notebook.index(nb.select())       # Should be either 1 or 0
        if (i == 0):
            table = self.main_tab       # Main tab selected
        elif (i == 1):
            table = self.ood_tab        # Out-of-date tab selected
        else:
            return None                 # Unknown tab selected, return None
        # If nothing is selected, return None
        if len(table.selection()) == 0:
            return None
        # Otherwise, get the fields in the table as a list
        fields = list(table.item(table.selection(), 'values'))
        # Get a list of all the freedges in the currently loaded database
        freedges = self.fdb.get_freedges()
        # Use the retrieved table fields to lookup the freedge by ID (field 0)
        selected = freedges[int(fields[0]) - 1]
        # Return the corresponding Freedge object
        return selected
        
    def OnTableClick(self, event: Event):
        """
        Update the GUI info_box when the user clicks on an entry in the table.
        
        Parameters:
            event:   A parameter required by tkinter, though it is not used
                     by this function.
        Returns: None
        """
        # Retrieve the Freedge currently selected in the GUI data table
        selected = self.GetSelected()
        if selected is not None:
            # Remove the previously displayed Freedge information
            self.info_label.destroy()
            # Create a new label for the newly selected Freedge's info
            self.info_label = ttk.Label(self.info_box, text=selected.ToString(),
                justify=LEFT, style='TLabel', width=self.ib_width)
            self.info_label.grid(sticky="ew", row=1)
    
    def NotifyFreedge(self, freedge: Freedge):
        """
        Sends a notification to the caretaker of the passed-in Freedge object.
        
        Returns: None
        """
        # Check that the passed-in argument is not None
        if freedge is None:
            return
        # Verify that the caretaker has consented to receiving messages
        if not freedge.can_notify():
            messagebox.showwarning("Permission Denied", "The selected freedge "
                "caretaker has not given permission to receive notifications.")
            return      # If not, notify the admin and return
        
        # Do not send messages to a freedge that is confirmed to be inactive
        if freedge.freedge_status == Status.ConfirmedInactive:
            messagebox.showwarning("Inactive Freedge", "The selected freedge "
                " has been previously confirmed as inactive.")
            return
        
        # Format the message based on the user's preferred contact method
        if (freedge.preferred_contact_method == ContactMethod.SMS.value):
            contact_type = "SMS"
            contact_string = "Phone number:\t" + freedge.phone_number + "\n"
        else:
            contact_type = "email"
            contact_string = "Email address:\t" + freedge.email_address + "\n"
        message = 'Do you want to check in with the selected freedge' \
            ' caretaker via {0}?\n\nProject name:\t{1}\nCaretaker ' \
            'name:\t{2}\n{3}Last update:\t{4} days ago.\n'.format(contact_type,
            freedge.project_name, freedge.caretaker_name, contact_string,
            freedge.time_since_last_update())
        
        # Confirm with the user (administrator) before sending the notification
        response = messagebox.askokcancel("Confirm Notification", message)
        if response:        # If the messagebox's reply value was 'True'
            # Create a new instance of the NoficationMgmt class
            notifier = NS.NotificationMgmt(self.root)
            # Use the new notifier to notify the freedge caretaker
            notifier.notify_and_update(self.fdb, freedge)
        # Update the display to reflect their response
        self.UpdateFullDisplay()
    
    def NotifySelected(self):
        """
        Sends a notification to the caretaker of the freedge that is currently
        selected by the user in the display table, if any.
        
        After retrieving the currently selected Freedge, the function calls
        NotifyFreedge() to actually send the notification.
        
        Returns: None
        """
        # Verify that a database has been loaded before proceeding
        if (self.fdb is None):
            return
        # Get the Freedge entry currently selected in the table
        selected: Freedge = self.GetSelected()
        if selected is None:
            return
        # Call NotifyFreedge to send a message to the freedge's caretaker
        self.NotifyFreedge(selected)

    def NotifyOutOfDate(self):
        """
        Sends a notification to each of the caretakers who have not been
        contacted in the amount of time defined by FIRST_UPDATE_THRESHOLD in
        the constants file (InternalData/database_constants.py).
        
        Returns: None
        """
        # Verify that a database has been loaded before continuing
        if (self.fdb is None):
            return
        # Retrieve the list of out of date freedges according to the database
        ood_list = self.fdb.get_out_of_date()
        # Create a list of freedges which can be notified based on whether they
        # have given permission to be notified, and are not confirmed to have
        # an inactive status.
        to_notify = []
        for freedge in ood_list:
            if freedge.freedge_status != Status.ConfirmedInactive.value:
                if freedge.can_notify():
                    to_notify.append(freedge)
        # If the list is empty, there are no out-of-date freedge statuses
        if (len(to_notify) == 0):
            messagebox.showinfo("No Caretakers to Notify",
                "All freedge statuses in the system are currently up to date.")
            return
        
        # Otherwise, build a message to show the user about the caretakers who
        # will be notiified.
        message = "It has been " + str(FIRST_UPDATE_THRESHOLD) + " or more" \
            " days since the following freedges statuses were updated:\n"
        for freedge in to_notify:
            message += "-------------------------------------------\n"
            message += "Project name:\t" + freedge.project_name + "\n"
            message += "Caretaker name:\t" + freedge.caretaker_name + "\n"
            message += "Phone number:\t" + freedge.phone_number + "\n"
            message += "Last update:\t" +\
                str(freedge.time_since_last_update()) + " days ago.\n"
            
        # Display information about the freedges the system will notify
        messagebox.showinfo("Caretaker Information", message)
        prompt = "The following caretakers will be contacted to request a" \
                 " status update:\n"
        for freedge in to_notify:
            prompt += "Name: " + freedge.caretaker_name + "\t"
            prompt += "Contact:\t" + freedge.phone_number + "\n"
        prompt += "\nHit 'ok' to confirm or 'cancel' to cancel."
        # Verify that the user (admin) would still like to send the messages
        response = messagebox.askokcancel("Verify Message", prompt)
        if response:
            for freedge in to_notify:
                notifier = NS.NotificationMgmt(self.root)
                notifier.notify_and_update(self.fdb, freedge)
        # Update the display to reflect any changes based on the responses
        self.UpdateFullDisplay()

    # =========================================================================
    # GUI Management Methods    (creation, updating)
    # =========================================================================

    def UpdateFullDisplay(self):
        """
        Updates the GUI display to reflect the currently loaded database
        information.
        
        Returns: None
        """
        # If no database has been loaded into the system yet, show the user
        # instructions on the next steps they could take.
        prompt = "No database loaded.\n\n Click 'Create Database' to create " \
            "a new freedge database from a csv file.\n\nClick 'Load " \
            "Database' to load in an existing database from a .db file."
        if (self.fdb is None):
            none_found = Label(self.notebook, text=prompt, anchor='center',
                               foreground="#e74c3c", background="#d4dadd",
                               width=50, wraplength=300, font=("Helvetica", 12))
            none_found.place(relx=0.5, rely=0.5, anchor='center')
            self.prompt_label = none_found
            return
        # Otherwise, get rid of the instruction prompt label if it exists
        elif self.fdb is not None and self.prompt_label is not None:
            self.prompt_label.destroy()
        # Get the list of freedges in the currently loaded database
        freedges = self.fdb.get_freedges()
        # Get the list of freedges whose statuses are considered out-of-date
        out_of_date = self.fdb.get_out_of_date()
        self.root.update()      # Be sure the display is up-to-date
        # Update the displays of the two GUI tabs, 'All' and 'Out of Date'
        self.UpdateTableDisplay(self.main_tab, freedges)
        self.UpdateTableDisplay(self.ood_tab, out_of_date)
    
    def UpdateTableDisplay(self, table: Treeview, freedges: [Freedge]):
        """
        Updates the information in a particular display table to contain the
        information stored in the array of Freedge objects passed in.
        
        Parameters:
            table: the tkinter Treeview object for the table to update.
            freedges: An array of Freedge objects containing the data to
                      fill the table with
                      
        Return: None
        """
        # clear the old list of freedges
        for item in table.get_children():
            table.delete(item)
        # Add the new list of freedges
        for fridge in range(len(freedges)):
            f = freedges[fridge]
            contact = "-"
            if (f.preferred_contact_method == ContactMethod.SMS.value):
                contact = f.phone_number
            if (f.preferred_contact_method == ContactMethod.Email.value):
                contact = f.email_address
            # Insert the Freedge's data into the Treeview display
            table.insert(parent='', index=fridge, iid=fridge, text='', values=(
                f.freedge_id, f.project_name, f.fridge_location.ShortString(),
                f.caretaker_name, f.freedge_status.value, f.last_status_update))

    def BuildTable(self, tab: Frame) -> Treeview:
        """
        Constructs a new tkinter Treeview to display a data table.
        
        Parameters:
            tab: a tkinter Frame to be the parent of the created Treeview.
        
        Returns: a tkinter Treeview (the table which was constructed)
        """
        # Build the structure of the Treeview's columns and their widths
        name_width_dict = {'FID': 40, 'Project Name': 240, 'Location': 200,
        'Owner': 150, 'Freedge Status': 150, 'Last Status Update': 100}
        columns = list(name_width_dict.keys())
        table = ttk.Treeview(tab, height=30, columns=columns, show='headings',
                             selectmode='browse')
        table.pack()
        
        # Insert the columns/headers for the table
        table.column('#0', width=0, stretch=NO)
        table.heading('#0', text='', anchor='w')
        for col in columns:
            table.column(col, anchor='w', width=name_width_dict[col])
            table.heading(col, anchor='w', text=col)
        # Bind the function OnTableClick() to be called when a row is selected
        table.bind('<<TreeviewSelect>>', self.OnTableClick)
        return table
    
    def AddButton(self, parent, label, cmd, xpos, ypos):
        """
        Adds a new button to the GUI.
        
        Parameters:
            parent: the tkinter object to be the parent of the new Button
            label: the str for the text to show on the Button
            cmd: the function to call when the Button is clicked on
            xpos: the x position to place the Button, relative to the parent
            ypos: the y position to place the Button, relative to the parent
        
        Returns: None
        """
        # The font family, font size, and display width for all the buttons
        font_style = "Helvetica"
        font_size = 10
        width = 15
        # Instantiate the button
        button = Button(parent, text=label, command=cmd, font=(font_style,
            font_size), width=width, justify=CENTER)
        # Place the button
        button.place(x=xpos, y=ypos)

    def CreateDisplay(self):
        """
        Builds the full tkinter GUI display of the Administrator Interface.
        
        Returns: None
        """
        # Initialize the root of the tkinter display
        root = Tk()
        root.title("Freedge Tracker")           # Title of application
        width = root.winfo_screenwidth()-100    # Width of application
        height = root.winfo_screenheight()-150  # Height of application
        root.geometry("%dx%d" % (width, height))
        
        root.wm_state('zoomed')             # Default to fill the screen
        root.configure(bg='#34495e')        # Set the background color
        self.root = root

        # Create a Header for the GUI display
        header = Label(root, width=50, text="Freedge Tracker",
            background="#34495e", foreground="white", font=("TkDefaultFont", 30))
        header.pack(side=TOP, padx=10, pady=30)
        header.place(x=100, y=40)

        # =====================================================================
        # Creating the Freedge Info Tables
        # =====================================================================
        # Create a tkinter Notebook to be the parent of the data tables
        notebook = Notebook(root, height=480, width=880)
        notebook.place(x=200, y=100)
        self.notebook = notebook
        # Create the two interactable tabs for the data table
        tab1 = Frame(notebook)
        notebook.add(tab1, text='    All    ')
        tab2 = Frame(notebook)
        notebook.add(tab2, text='Out of Date')

        # Build the structure of the tables to be displayed in the two tabs
        self.main_tab = self.BuildTable(tab1)
        self.ood_tab = self.BuildTable(tab2)
        
        # Create the display to provide info about the currently selected row
        info_box = Frame(root, height=514, width=30)
        info_box.place(x=1160, y=160)
        self.info_box = info_box
        # Title/header of the display box
        label = ttk.Label(info_box, text="Selected Freedge Information",
                        style='TFrame.TLabel', width=self.ib_width)
        label.columnconfigure(0, weight=1)
        label.grid(column=0, row=0, sticky="ew")
        # The Label to use to display the actual data
        info_label = ttk.Label(info_box, width=self.ib_width)
        self.info_label = info_label
        info_label.grid(column=0, row=1, sticky="ew")
        info_label.columnconfigure(0, weight=1)
        info_label.rowconfigure(1, weight=1)

        # =====================================================================
        # Creating the GUI Buttons
        # =====================================================================
        block1 = Frame(root, height=150, width=150, background="#34495e")
        block1.place(x=30, y=100)
        # Button to Create new database (db)
        self.AddButton(block1, "Create Database", self.CreateDatabase, 10, 10)
        # Button to load a database
        self.AddButton(block1, "Load Database", self.SelectAndOpenDB, 10, 60)

        block2 = Frame(root, height=220, width=150, background="#34495e")
        block2.place(x=30, y=300)
        # Button to notify selected freedge
        self.AddButton(block2, "Notify Selected", self.NotifySelected, 10, 10)
        
        # Button to notify all out-of-date freedges
        self.AddButton(block2, "Notify Out-Of-Date", self.NotifyOutOfDate, 10, 60)

        block3 = Frame(root, height=220, width=150, background="#34495e")
        block3.place(x=30, y=500)
        # Button to exit session
        self.AddButton(block3, "Exit", self.exit_, 10, 10)
        
        # =====================================================================
        # Configure the style of the display
        # =====================================================================
        style = build_style()
        style.theme_use("freedge_theme")

    def exit_(self):
        """
        Ends and exits the program.
        
        Is called the when user clicks on the corresponding 'exit' button
        in the GUI display.

        Returns: None
        """
        # use the exit method from the sys module
        sys.exit()
