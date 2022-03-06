"""
===============================================================================
Title:	The Tkinter Display Style for the Administrator Interface's GUI
===============================================================================
Description:	This is a file containing a function to build the tkinter
				display style for the system's GUI.

Authors:        Madison Werries
Last Edited:    3-5-2022
Last Edit By:   Madison Werries

"""
from tkinter.ttk import *
from admin_interface.administrator_interface import *
def build_style():
	"""
	Builds the tkinter style for the Administrator Interface GUI.
	
	Returns: a tkinter Style.
	"""
	# Colors for the GUI display
	bg_color = "#bdc3c7"
	light_base = "#ecf0f1"
	gold_color = "#ffcd02"
	color_tab = "#ccdee0"
	
	# Create a style for the display to help prevent messy code by defining
	# all the style elements for each individual tkinter object
	style = Style()
	default_font = 'Helvetica'
	
	style.theme_create("freedge_theme", parent="default", settings={
		"TNotebook": {"configure": {
			"padding": [30, 5],
			"tabmargins": [0, 10, 20, 10],
			"background": bg_color,
			"borderwidth": [0],
			"highlightthickness": [0]}},
		"TNotebook.Tab": {"configure": {
			"padding": [30, 5],
			"background": bg_color,
			"font": (default_font, 14),
			"borderwidth": [0]},
			"map": {
				"background": [("selected", gold_color),
							   ('!active', "lightgrey"), ('active', color_tab)],
				"expand": [("selected", [1, 1, 1, 0])]}},
		"TFrame": {"configure": {
			"borderwidth": [0],
			"highlightthickness": [0]}},
		"TFrame.TLabel": {"configure": {
			"font": (default_font, 14),
			"foreground": "orange",
			"background": "dimgray"}
		},
		"TLabel": {"configure": {
			"font": (default_font, 10),
			"foreground": "dimgray",
			"background": "white"}
		},
		"Treeview.Heading": {
			"configure": {
				"font": (default_font, 12),
				"foreground": "orange",
				"background": "dimgray"}},
		'Treeview': {
			"configure": {
				"fieldbackground": "#bdc3c7",
				"borderwidth": [0],
				"highlightthickness": [0]},
			'map': {
				'background': [('!selected', light_base), ('selected', 'white')],
				'font': [('selected', ("Century Gothic", 10, 'bold'))],
			}
		},
		".": {
			"configure": {"font": (default_font, 10), "foreground": "gray"}
		}
	})
	return style

