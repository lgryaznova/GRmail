## GRmail usage notes

*start.py* is a script used to start the application.

*root.py* initilizes tkinter and sets up its environment. It is used by *start.py, mainwindow.py* (the latter needs root object for 'Quit' button.

*base_cls.py* contains abstract base classes for tkinter.

*mainwindow.py* contains MainWindow class describing the application's main window tab.

*addressbook.py* contains AddressBook class describing the application's addressbook tab.

*settings.py* contains Settings class describing the application's settings tab (logic is not yet implemented).

*autocomplete.py* contains AutocompleteCombobox class.

*data_cls.py* contains classes needed for data of the app.

*pickle files (.pkl)* are used to store data.

*helper.py* contains helper functions.

*edit-icon.gif* is the picture used by the app, required.

*example_data.py* is not required for the work of the applicatin. It is a script to prepare pickle files used by the application. The files contain labels and texts, as well as information about users, departments and regions. The script is included to demonstrate data structures used by the app.
