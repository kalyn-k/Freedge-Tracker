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


class admin_interface:
    def __init__(self):
        pass

    def NewDatabase(self, event=None):
        filename = filedialog.askopenfilename()
        # TODO how can i get the db_path?
        pass

    def UpdateDatabase(self, event=None):
        filename = filedialog.askopenfilename()
        # TODO how can i get the db_path?
        pass

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
        menu.title(" Freedge Tracker ")  # TODO do we wanna change the title?
        # Sets window size
        menu.geometry("500x750")
        # Prevent the menu window from being resized
        menu.resizable(False, False)
        # Set menu background color
        menu.configure(bg='black')

        # Button to Create new database (db)
        create_db_button = Button(menu, text="Create new Database", font=("TkDefaultFont", 20),
                             bg="white", width=20)  # initiate the button
        create_db_button.pack(padx=10, pady=10)

        # Button to update database
        update_db_button = Button(menu, text="Update Database", font=("TkDefaultFont", 20),
                             bg="white", width=20)  # initiate the button
        update_db_button.pack(padx=10, pady=10)

        # Button to exit session
        exit_button = Button(menu, text="            Exit           ", font=("TkDefaultFont", 20), command=self.exit_,
                             bg="white", width=20)  # initiate the button
        exit_button.pack(padx=10, pady=10)


        # TODO: the buttons to be added: Create Graph (?), ...

        menu.mainloop()


if __name__ == '__main__':
    screen = admin_interface()
    screen.MenuDisplay()
