"""
Base tkinter classes (Application, StandardTab)
"""
import tkinter.ttk as ttk
import sys

class Application(ttk.Notebook):
    """
    Frame of the application, contains tabs
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0)


class StandardTab(ttk.Frame):
    """
    Abstract class for tabs of the application
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0)
        self.create_widgets()

        # keypress on Return moves focus to the next field
        self.bind_class('Entry', '<Return>', self.focus_next_window)
        self.bind_class('Combobox', '<Return>', self.focus_next_window)
        self.bind_class('Text', '<Control-Return>', self.focus_next_window)

    def create_widgets(self):
        """
        Method to be overridden by instances
        """
        raise NotImplementedError

    def focus_next_window(self, event):
        """
        Helper function to change focus on widgets using
        specified key button.
        From here: http://stackoverflow.com/a/1451343
        """
        event.widget.tk_focusNext().focus()
        return ("break")

    def update_list(self, widget_name, new_list):
        """
        Updates list of users or regions if amended
        """
        self.nametowidget(widget_name)['values'] = new_list
        try:
            self.nametowidget(widget_name).set_completion_list(new_list)
        except AttributeError:
            return
