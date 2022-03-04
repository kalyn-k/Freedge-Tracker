"""
===============================================================================
Title:	Administrator Interface for the Freedge Tracker System
===============================================================================
Description:	This is the Administrator Interface module for the Freedge
                Tracker System. It is the main driver for the system, and
                is responsible for both I/O from an administrator and the
                GUI display to the admin (the user).
                
Authors:        Kalyn Koyanagi, Madison Werries
Last Edited:    3-4-2022
Last Edit By:   Madison Werries
"""
from tkinter.ttk import *
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import sys
import Notification_System as NS
from Freedge_Database import *

class AdministratorInterface:
    def __init__(self):
        """
        Initializes a new instance of the AdministratorInterface class.
        """
        # =====================================================================
        # Information about the currently loaded database.
        # =====================================================================
        self.fdb_path = None        # The file path to the internal database
        self.fdb = None             # The FreedgeDatabase object

        # =====================================================================
        # GUI elements which need to be accessed later on:
        # =====================================================================
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
    # I/O for Administrator Interface
    # =========================================================================

    def LoadDatabase(self):
        file_types = [('db files', '.db')]
        prompt = "Please select the .db file to load into the system."
        messagebox.showinfo("Select internal database location", prompt)
        db_file_path = filedialog.askopenfilename(
            title="Please select the internal database file.",
            filetypes=file_types, defaultextension=".db")
        # If they provided a filename correctly
        if (db_file_path != ""):
            self.OpenDatabase(db_file_path)
        # Update the display tables
        self.UpdateFullDisplay()
    
    def OpenDatabase(self, db_file_path):
        # Create a new database using the data from the CSV file
        self.fdb_path = db_file_path
        self.fdb = load_internal_database(db_file_path)
        # Set the path of the most recently accessed database:
        saved_fdb_path = open("Internal_Data/fdb_path.txt", "w+")
        saved_fdb_path.write("This is a text file which contains the file path to"
                             " the last database(.db file) that was opened.\n")
        saved_fdb_path.write(self.fdb_path)
        saved_fdb_path.close()
    
    def SaveDatabase(self, csv_file_path):
        file_types = [('db files', '.db')]
        prompt = "Please select where you would like to save the internal database file."
        messagebox.showinfo("Select internal database location", prompt)
        db_file_path = filedialog.asksaveasfilename(
            title="Please select where to save the internal .db file to",
            filetypes=file_types, defaultextension=".db")
        # If they provided a filename correctly
        if (db_file_path != ""):
            # Create a new database using the data from the CSV file
            self.fdb_path = db_file_path
            self.fdb = new_database_from_csv(db_file_path, csv_file_path)
            # Set the path of the most recently accessed database:
            saved_fdb_path = open("Internal_Data/fdb_path.txt", "w+")
            saved_fdb_path.write("This is a text file which contains the file path to"
                                 " the last database(.db file) that was opened.\n")
            saved_fdb_path.write(self.fdb_path)
            saved_fdb_path.close()
    
    def NewDatabase(self):
        prompt = "Please select the csv file you would like to use to create a new freedge database."
        # Get the path of CSV file from the user
        user_response = messagebox.showinfo("Please Select a CSV file", prompt)
        if user_response is None or not user_response:
            return
        file_types = [('csv files', '.csv')]
        continue_prompts = True
        while continue_prompts:
            csv_file_path = filedialog.askopenfilename(title="Please select the csv"
                " file containing the freedge data.", filetypes=file_types)
            if (csv_file_path is None or csv_file_path == ""):
                answer = messagebox.askretrycancel("Question", "Error: No file selected.")
                # If the user hit 'Cancel' or 'X', discontinue the prompts,
                # and do not create a new database file
                if (answer is None or not answer):
                    continue_prompts = False
                    continue
            else:
                continue_prompts = False
                self.SaveDatabase(csv_file_path)
                # Update the display with the newly loaded data
                self.UpdateFullDisplay()

    def UpdateDatabase(self, event=None):
        # Get path of CSV file
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
        
    def GetSelected(self):
        nb = self.notebook
        i = nb.index(nb.select())
        table = None
        if (i == 0):
            table = self.main_tab
        elif (i == 1):
            table = self.ood_tab
        if len(table.selection()) == 0:
            return None
        fields = list(table.item(table.selection(), 'values'))
        freedges = self.fdb.get_freedges()
        selected = freedges[int(fields[0]) - 1]
        return selected
        
    def OnTableClick(self, event):
        """ What to do when the administrator clicks on a freedge in the display table. """
        selected = self.GetSelected()
        self.info_label.destroy()
        self.info_label = ttk.Label(self.info_box, text=selected.ToString(),
            justify=LEFT, style='TLabel', width=self.ib_width)
        self.info_label.grid(sticky="ew", row=1)
    
    def NotifyFreedge(self, freedge):
        if (self.fdb is None):
            return
        if freedge is None:
            print("nothing is selected!")
            return
        if not freedge.can_notify():
            messagebox.showwarning("Permission Denied", "The selected freedge "
                "caretaker has not given permission to receive notifications.")
            return
        
        if (freedge.preferred_contact_method == ContactMethod.SMS.value):
            message = "Do you want to check in with the selected freedge caretaker via SMS?\n\n"
            message += "Project name:\t" + freedge.project_name + "\n"
            message += "Caretaker name:\t" + freedge.caretaker_name + "\n"
            message += "Phone number:\t" + freedge.phone_number + "\n"
            message += "Last update:\t" + str(freedge.time_since_last_update()) + " days ago.\n"
        else:
            message = "Do you want to check in with the selected freedge caretaker via email?\n\n"
            message += "Project name:\t" + freedge.project_name + "\n"
            message += "Caretaker name:\t" + freedge.caretaker_name + "\n"
            message += "Email:\t" + freedge.email_address + "\n"
            message += "Last update:\t" + str(freedge.time_since_last_update()) + " days ago.\n"
        
        response = messagebox.askokcancel("Confirm Notification", message)
        if response:
            notifier = NS.NotificationMgmt(self.root)
            notifier.notify_and_update(self.fdb, freedge)
        self.UpdateFullDisplay()
      
    def NotifySelected(self):
        if (self.fdb is None):
            return
        # Get the currently selected Freedge entry
        selected: Freedge = self.GetSelected()
        if selected is None:
            print("nothing is selected!")
            return
        if not selected.can_notify():
            messagebox.showwarning("Permission Denied", "The selected freedge "
                "caretaker has not given permission to receive notifications.")
            return
        self.NotifyFreedge(selected)
        self.UpdateFullDisplay()

    def NotifyAll(self):
        if (self.fdb is None):
            return
        # TODO
        print("notifying all freedges")
    
    def NotifyOutOfDate(self):
        if (self.fdb is None):
            return
        ood_list = self.fdb.get_out_of_date()
        to_notify = []
        for freedge in ood_list:
            if freedge.can_notify():
                to_notify.append(freedge)
        
        if (len(to_notify) == 0):
            messagebox.showinfo("No Caretakers to Notify",
                "All freedge statuses in the system are currently up to date.")
            return
        message = "It has been " + str(FIRST_UPDATE_THRESHOLD) + " or more days" \
            " since the following freedge caretakers were prompted for status updates:\n"
        for freedge in to_notify:
            message += "-------------------------------------------\n"
            message += "Project name:\t" + freedge.project_name + "\n"
            message += "Caretaker name:\t" + freedge.caretaker_name + "\n"
            message += "Phone number:\t" + freedge.phone_number + "\n"
            message += "Last update:\t" + str(freedge.time_since_last_update()) + " days ago.\n"

        messagebox.showinfo("Caretaker Information", message)
        prompt = "The following caretakers will be contacted to request a status update:\n"
        for freedge in to_notify:
            prompt += "Name: " + freedge.caretaker_name + "\t"
            prompt += "Contact:\t" + freedge.phone_number + "\n"
        prompt += "\nHit 'ok' to confirm or 'cancel' to cancel."
       
        response = messagebox.askokcancel("Verify Message", prompt)
        
        if response:
            for freedge in to_notify:
                notifier = NS.NotificationMgmt(self.root)
                notifier.notify_and_update(self.fdb, freedge)
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

    # =========================================================================
    # GUI for Administrator Interface
    # =========================================================================

    def UpdateFullDisplay(self):
        if (self.fdb is None):
            prompt = "No database loaded.\n\n" \
                     "Click 'New Database' to create a new freedge database from a csv file." \
                     "\n\nClick 'Load Database' to load in an existing database from a .db file."
            none_found = Label(self.notebook, text=prompt, anchor='center', foreground="#e74c3c",
                               background="#d4dadd", width=50, wraplength=300, font=("Helvetica", 12))
            none_found.place(relx=0.5, rely=0.5, anchor='center')
            self.prompt_label = none_found
            return
        else:
            if self.prompt_label is not None:
                self.prompt_label.destroy()
        
        freedges = self.fdb.get_freedges()
        out_of_date = self.fdb.get_out_of_date()
        self.root.update()
        self.UpdateTableDisplay(self.main_tab, freedges)
        self.UpdateTableDisplay(self.ood_tab, out_of_date)
    
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
                f.freedge_id, f.project_name, f.fridge_location.ShortString(),
                f.caretaker_name, f.freedge_status.value, f.last_status_update))

    def BuildTable(self, tab):
        # Structure the table view of the Freedges
        columns = ('FID', 'Project Name', 'Location', 'Owner', 'Freedge Status',
                   'Last Status Update')
        table = ttk.Treeview(tab, height=30, columns=columns, show='headings', selectmode='browse')
        table.place(x=0, y=0)
        table.pack()
        ttk.Style().configure("Treeview", background="black",
                              foreground="black", fieldbackground="black")
        # Insert the columns
        table.column('#0', width=0, stretch=NO)
        table.column('FID', anchor='w', width=40)
        table.column('Project Name', anchor='w', width=240)
        table.column('Location', anchor='w', width=200)
        table.column('Owner', anchor='w', width=150)
        table.column('Freedge Status', anchor='w', width=150)
        table.column('Last Status Update', anchor='w', width=100)
    
        # Insert the headers
        table.heading('#0', text='', anchor='w')
        table.heading('FID', anchor='w', text='FID')
        table.heading('Project Name', anchor='w', text='Project Name')
        table.heading('Location', anchor='w', text='Location')
        table.heading('Owner', anchor='w', text='Owner')
        table.heading('Freedge Status', anchor='w', text='Freedge Status')
        table.heading('Last Status Update', anchor='w', text='Last Update')
        
        table.tag_configure("odd_row", anchor='w', background="white")
        table.tag_configure("even_row", anchor='w', background="red")

        table.bind('<<TreeviewSelect>>', self.OnTableClick)
        return table
    
    def AddButton(self, parent, label, cmd, xpos, ypos):
        font_style = "Helvetica"
        font_size = 10
        width = 15
        button = Button(parent, text=label, command=cmd, font=(font_style,
            font_size), width=width, justify=CENTER)
        button.place(x=xpos, y=ypos)

    def CreateDisplay(self):
        # Initialize the display for the Administrator Interface
        root = Tk()
        root.title("Freedge Tracker")
        width = root.winfo_screenwidth()-100
        height = root.winfo_screenheight()-150
        root.geometry("%dx%d" % (width, height))
        root.wm_state('zoomed')
        root.configure(bg='#34495e')      # Set menu background color
        root.maxsize()
        self.root = root

        # Create a Header for the menu
        header = Label(root, width=50, text="Freedge Tracker", background="#34495e", foreground="white",
                       font=("TkDefaultFont", 30))
        header.pack(side=TOP, padx=10, pady=30)
        header.place(x=100, y=40)

        # =====================================================================
        # Creating the Freedge Info Tables
        # =====================================================================
        # Tabs for the table (https://www.geeksforgeeks.org/creating-tabbed-widget-with-python-tkinter/)
        notebook = Notebook(root, height=480, width=880)
        tab1 = Frame(notebook)
        tab2 = Frame(notebook)
        notebook.add(tab1, text='    All    ')
        notebook.add(tab2, text='Out of Date')
        notebook.place(x=200, y=100)
        self.notebook = notebook

        # Build the tables to be displayed in the two tabs
        self.main_tab = self.BuildTable(tab1)
        self.ood_tab = self.BuildTable(tab2)
        
        # Create the display box to show the admin more info about a selected freedge in the table
        info_box = Frame(root, height=514, width=30)
        info_box.place(x=1160, y=160)
        self.info_box = info_box
        label = ttk.Label(info_box, text="Selected Freedge Information",
                        style='TFrame.TLabel', width=self.ib_width)
        label.columnconfigure(0, weight=1)
        label.grid(column=0, row=0,sticky="ew")
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
        self.AddButton(block1, "Create Database", self.NewDatabase, 10, 10)
        # Button to update database
        self.AddButton(block1, "Load Database", self.LoadDatabase, 10, 60)

        block2 = Frame(root, height=220, width=150, background="#34495e")
        block2.place(x=30, y=300)
        # Button to notify selected freedge
        self.AddButton(block2, "Notify Selected", self.NotifySelected, 10, 10)
        
        # Button to notify all out-of-date freedges
        self.AddButton(block2, "Notify Out-Of-Date", self.NotifyOutOfDate, 10, 60)

        # Button to send a message to all freedges
        self.AddButton(block2, "Notify All", self.NotifyAll, 10, 110)

        block3 = Frame(root, height=220, width=150, background="#34495e")
        block3.place(x=30, y=500)
        # Button to exit session
        self.AddButton(block3, "Exit", self.exit_, 10, 10)
        
        # =====================================================================
        # Configure the style of the display
        # =====================================================================
        # Colors for the GUI display
        bg_color = "#bdc3c7"
        light_base = "#ecf0f1"
        gold_color = "#ffcd02"
        color_tab = "#ccdee0"
        
        # style
        style = Style()
        default_font = 'Helvetica'
        
        style.theme_create("freedge_theme", parent="default", settings={
            "TNotebook": {
                "configure": {"padding": [30, 5], "tabmargins": [0, 10, 20, 10], "background": bg_color,
                              "borderwidth": [0], "highlightthickness": [0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [30, 5], "background": bg_color, "font": (default_font, 14),
                              "borderwidth": [0]},
                "map": {"background": [("selected", gold_color), ('!active', "lightgrey"), ('active', color_tab)],
                        "expand": [("selected", [1, 1, 1, 0])]}},
            "TFrame": {
                "configure": {"borderwidth": [0], "highlightthickness": [0]}},
            "TFrame.TLabel": {
                "configure": {"font": (default_font, 14), "foreground": "orange", "background": "dimgray"}
            },
            "TLabel": {
                "configure": {"font": (default_font, 10), "foreground": "dimgray", "background": "white"}
            },
            "Treeview.Heading": {
                "configure": {"font": (default_font, 12), "foreground": "orange", "background": "dimgray"}},
            'Treeview': {
                "configure": {"fieldbackground": "#bdc3c7", "borderwidth": [0], "highlightthickness": [0]},
                'map': {
                    'background': [('!selected', light_base), ('selected', 'white')],
                    'font': [('selected', ("Century Gothic", 10, 'bold'))],
                }
            },
            ".": {
                "configure": {"font": (default_font, 10), "foreground": "gray"}
            }
        })
        style.theme_use("freedge_theme")
        

if __name__ == '__main__':
    # Create a new Administrator Interface
    MainInterface = AdministratorInterface()
    # Build the Administrator Interface's GUI
    MainInterface.CreateDisplay()
    
    # Check whether or not an internal database already exists. This
    # information is stored using the file: "Internal_Data/fdb_path.txt"
    try:
        # Check that the file "Internal_Data/fdb_path.txt" exists
        path_location = open("Internal_Data/fdb_path.txt", "r")
    except IOError:
        # If there's an error and the internal file does not exist, create it
        path_location = open("Internal_Data/fdb_path.txt", "w+")
        # Write a header briefly describing the file
        path_location.write("This is a text file which contains the file path"
                            " to the last database (.db file) that was opened.")
        # Write a blank line to be filled with the file path later
        path_location.write("")
    
    # Read the lines in from the internal file
    lines = path_location.readlines()
    db_file_found = False               # Whether we successfully find a .db file
    located_file_path = ""              # The path to the .db file, if one is found
    path_location.close()
    # If the number of lines is less than 2, there is no file path specified
    if (len(lines) >= 2):
        # The first line is the header, the second is the file location
        located_file_path = lines[1]
        db_file_found = exists_internal_database(located_file_path)
    
    # Ensure that the dialogue boxes will be shown
    MainInterface.root.update()
    
    # If an internal database file was found...
    if (db_file_found):
        # Prompt the user for whether they want to use the (.db) file found
        title = "An existing database was found at: " + located_file_path + \
                ".\n\nWould you like to proceed with that database?"
        response = messagebox.askyesno("Database Found", title)
        # If they gave a response (ie, didn't just hit 'X')...
        if (response is not None):
            if response:
                # Otherwise, load the internal database file that was found
                MainInterface.fdb_path = located_file_path
                MainInterface.OpenDatabase(located_file_path)
    MainInterface.UpdateFullDisplay()
    MainInterface.root.mainloop()

