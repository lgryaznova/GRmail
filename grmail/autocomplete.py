"""
AutocompleteCombobox class
"""

import tkinter as tk
import tkinter.ttk as ttk

class AutocompleteCombobox(ttk.Combobox):
    """
    From here: http://code.activestate.com/lists/python-tkinter-discuss/3010/
    """
    def set_completion_list(self, completion_list):
        """Use our completion list as our drop down selection menu,
        arrows move through menu."""
        # Work with a sorted list
        self._completion_list = sorted(completion_list, key=str.lower)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle
        through possible hits"""
        # need to delete selection otherwise we would fix the current position
        if delta:
            self.delete(self.position, tk.END)
        # set position to end so selection starts where textentry ended
        else:
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            # Match case insensitively
            if element.lower().startswith(self.get().lower()):
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)

        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END):  # delete the selection
                self.delete(self.position, tk.END)
            else:
                self.position = self.position - 1  # delete one character
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)  # go to end (no selection)
        # to exclude control keys    
        if event.keysym_num < 65000:
            self.autocomplete()
            # No need for up/down, we'll jump to the popup
            # list at the position of the autocompletion
