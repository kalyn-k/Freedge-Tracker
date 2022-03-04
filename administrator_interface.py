"""
===============================================================================
Title:	Administrator Interface for the Freedge Tracker System
===============================================================================
Description:	TODO
Authors:        Kalyn Koyanagi, Madison Werries
Last Edited:    3-2-2022
Last Edit By:   Madison Werries
"""
import tkinter
from tkinter import ttk, messagebox, filedialog
from tkinter import *
from tkinter.ttk import Notebook
import sys
import Notification_System as NS
from Freedge_Database import *

class AdministratorInterface:
    def __init__(self):
        """
        TODO
        """
        # Define user windows for later use
        self.fdb = None         # Connection to Freedge database
        self.main_tab = None    # All freedges tab
        self.ood_tab = None     # Out of date freedges tab
        self.root = None
        self.notebook = None
        self.info_box = None
    
    # =========================================================================
    # I/O for Administrator Interface
    # =========================================================================
    
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
        self.fdb = new_database_from_csv(DATABASE_PATH, file_path)
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
        print(selected.ToString())
        self.info_box.destroy()
        self.info_box = ttk.Label(self.selected_info, text=selected.ToString(), justify=LEFT, style='TLabel', width=50)
        self.info_box.grid(sticky=tkinter.S, row=1)
        print('boop')
    
    def NotifyFreedge(self, freedge):
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
        else:
            return
      
    def NotifySelected(self):
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
        
    def NotifyAll(self):
        # TODO
        print("notifying all freedges")
    
    def NotifyOutOfDate(self):
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
                print(freedge.caretaker_name)
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
        freedges = self.fdb.get_freedges()
        out_of_date = self.fdb.get_out_of_date()
        self.root.update()
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
        self.root = root

        # Create a Header for the menu
        header = Label(root, width=50, text="Freedge Tracker", bg="gray", fg="white",
                       font=("TkDefaultFont", 30))
        header.pack(side=TOP, padx=10, pady=30)

        # =====================================================================
        # Creating the Freedge Info Tables
        # =====================================================================
        # Tabs for the table (https://www.geeksforgeeks.org/creating-tabbed-widget-with-python-tkinter/)
        notebook = Notebook(root, height=480)
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
        selected_info = Frame(root, height=514, width=30)
        selected_info.place(x=1150, y=100)
        self.selected_info = selected_info
        label = ttk.Label(selected_info, text="Selected Freedge Information", justify=CENTER, style='TFrame.TLabel', width=30)
        label.pack(fill='both', expand=True)
        label.grid(column=0, row=0)
        selected_info.columnconfigure(0, weight=1)
        selected_info.rowconfigure(0, weight=1)
        
        label.grid(sticky=tkinter.NW, row=0)
        woop = ttk.Label(selected_info, text="fajalfjslfjslfjslfsj", justify=LEFT, style='TFrame.TLabel')
        self.info_box = woop
        # =====================================================================
        # Creating the GUI Buttons
        # =====================================================================
        # Button to Create new database (db)
        create_db_button = Button(root, text="Create new Database", font=("TkDefaultFont", 12),
                                  command=self.NewDatabase,
                                  bg="white", width=15)  # initiate the button
        create_db_button.place(x=30, y=180)

        # Button to update database
        update_db_button = Button(root, text="Update Database", font=("TkDefaultFont", 12), command=self.UpdateDatabase,
                                  bg="white", width=15)  # initiate the button
        update_db_button.place(x=30, y=230)

        # Button to notify selected freedge
        notif_selected = Button(root, text="Notify Selected", font=("TkDefaultFont", 12), command=self.NotifySelected,
                             bg="white", width=15)  # initiate the button
        notif_selected.place(x=30, y=300)
        
        # Button to notify all out-of-date freedges
        notif_ood = Button(root, text="Notify Out-Of-Date", font=("TkDefaultFont", 12), command=self.NotifyOutOfDate,
                             bg="white", width=15)  # initiate the button
        notif_ood.place(x=30, y=350)

        # Button to send a message to all freedges
        exit_button = Button(root, text="Notify All", font=("TkDefaultFont", 12),
                             command=self.NotifyAll,
                             bg="white", width=15)  # initiate the button
        exit_button.place(x=30, y=400)
        
        # Button to exit session
        exit_button = Button(root, text="            Exit           ", font=("TkDefaultFont", 12), command=self.exit_,
                             bg="white", width=15)  # initiate the button
        exit_button.place(x=30, y=500)
        
        # =====================================================================
        # Configure the style of the display
        # =====================================================================
        # Notebook color
        bg_color = "darkgrey"
        gold_color = "gold"
        color_tab = "#ccdee0"
        
        # style
        style = ttk.Style()
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
                "configure": {"background": "black", "borderwidth": [0], "highlightthickness": [0]}},
            "TFrame.TLabel": {
                "configure": {"font": (default_font, 14), "foreground": "orange", "background": "dimgray"}
            },
            "TLabel": {
                "configure": {"font": (default_font, 10), "foreground": "white", "background": "dimgray"}
            },
            "Treeview.Heading": {
                "configure": {"font": (default_font, 12), "foreground": "orange", "background": "dimgray"}},
            'Treeview': {
                "configure": {"fieldbackground": "darkgrey", "borderwidth": [0], "highlightthickness": [0]},
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
            self.root.update()
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
    screen = AdministratorInterface()
    screen.MenuDisplay()

