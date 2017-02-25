"""
Start the application
"""
from root import root
from base_cls import Application
from mainwindow import MainWindow
from addressbook import AddressBook
from settings import Settings
from helper import labels

# start app
app = Application(master=root)
main_window = MainWindow(master=app)
address_book = AddressBook(master=app)
settings_tab = Settings(master=app)
app.add(main_window, text=labels['main'])
app.add(address_book, text=labels['address_book'])
app.add(settings_tab, text=labels['settings'])
app.mainloop()
