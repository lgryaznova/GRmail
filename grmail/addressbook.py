"""
AddressBook class
"""
import tkinter as tk
import tkinter.ttk as ttk
from autocomplete import AutocompleteCombobox
from base_cls import StandardTab
from data_cls import User, Department, Region
from helper import labels, users, dept, regions
from helper import resource_path, logic_decorator

class AddressBook(StandardTab):
    """
    Second tab: address book
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0)
        self._user_current = None
        self._cf_func = None
        self._region_current = None
        self._clicked = False
        self._prev = None
        self.create_widgets()

    def create_widgets(self):
        """
        Create widgets
        """
        ############################################################
        # LEFT PANE
        ############################################################
        # fill in form
        self.left_pane = ttk.LabelFrame(
            self, text=labels['choose_to_modify'], width=30)
        self.left_pane.grid(row=0, column=0, columnspan=3, rowspan=5,
                            sticky='news', padx=10, pady=10)
        self.left_pane.columnconfigure(2, minsize=10)

        # prepare image for Edit button
        self.edit_image = tk.PhotoImage(file=resource_path('edit-icon.gif'))

        # choose user
        self.username_label = ttk.Label(self.left_pane,
                                        text=labels['username'])
        self.username_label.grid(row=0, column=0, sticky='en', pady=5, padx=2)
        self.username = ttk.Combobox(
            self.left_pane, values=users.keys(),
            state='readonly', font=('Arial', 13), width=25,
            postcommand=lambda: self.update_list(str(self.username),
                                                 users.keys()))
        self.username.grid(row=0, column=1, sticky='news', pady=5)
        self.username_button = ttk.Button(
            self.left_pane, image=self.edit_image,
            command=self.edit_user_pane, width=2)
        self.username_button.grid(row=0, column=2, sticky='news',
                                  pady=5, padx=2)

        # add a new user
        self.add_user_button = ttk.Button(
            self.left_pane, text=labels['add_user'],
            command=self.add_user_pane)
        self.add_user_button.grid(row=1, column=1, sticky='news', pady=5)

        # CF directors
        self.cf_directors_label = ttk.Label(self.left_pane,
                                            text=labels['cf_directors'])
        self.cf_directors_label.grid(row=2, column=0, sticky='en',
                                     pady=5, padx=2)
        self.cf_directors = ttk.Combobox(
            self.left_pane, values=dept.keys(),
            state='readonly', font=('Arial', 13))
        self.cf_directors.grid(row=2, column=1, sticky='news', pady=5)
        self.cf_directors_button = ttk.Button(
            self.left_pane, width=2, image=self.edit_image,
            command=self.open_dept_pane)
        self.cf_directors_button.grid(row=2, column=2, sticky='news',
                                      pady=5, padx=2)

        # enter region
        self.region_label = ttk.Label(self.left_pane, text=labels['region'])
        self.region_label.grid(row=3, column=0, sticky='en', pady=5, padx=2)
        self.region = AutocompleteCombobox(
            self.left_pane, font=('Arial', 13),
            postcommand=lambda: self.update_list(str(self.region),
                                                 regions.keys()))
        self.region.set_completion_list(regions.keys())
        self.region.bind("<Return>", self.focus_next_window)
        self.region.grid(row=3, column=1, sticky='news', pady=5)
        self.region_button = ttk.Button(self.left_pane, image=self.edit_image,
                                        width=2, command=self.edit_region_pane)
        self.region_button.grid(row=3, column=2, sticky='news', pady=5, padx=2)

        # add a new region
        self.add_region_button = ttk.Button(
            self.left_pane, text=labels['add_region'],
            command=self.add_region_pane)
        self.add_region_button.grid(row=4, column=1, sticky='news', pady=5)

        # warning message area
        self.warning_area = ttk.Label(self.left_pane, text='',
                                      style='Red.TLabel', wraplength=390)
        self.warning_area.grid(row=6, column=0, columnspan=3, rowspan=2,
                               padx=5, pady=50)

        ############################################################
        # RIGHT PANE
        ############################################################
        # edit section
        self.right_pane = ttk.LabelFrame(self)

        # edit user
        self.username_edit_label = ttk.Label(self.right_pane,
                                             text=labels['fullname'])
        self.username_edit = ttk.Entry(self.right_pane, font=('Arial', 13))

        self.email_label = ttk.Label(self.right_pane, text=labels['email'])
        self.email = ttk.Entry(self.right_pane, font=('Arial', 13))

        self.user_signature_label = ttk.Label(self.right_pane,
                                              text=labels['user_signature'])
        self.user_signature = tk.Text(
            self.right_pane, height=10, width=38, bd=1,
            highlightcolor='#6fa8d8', font=('Arial', 11), wrap='word',
            highlightbackground='#bcbcbc')
        self.scroll_signature = ttk.Scrollbar(self.right_pane)
        self.scroll_signature['command'] = self.user_signature.yview
        self.user_signature['yscrollcommand'] = self.scroll_signature.set

        # edit directors
        self.lastname_label = ttk.Label(self.right_pane,
                                        text=labels['lastname'])
        self.lastname = ttk.Entry(self.right_pane, font=('Arial', 13),
                                  width=35)

        self.firstname_label = ttk.Label(self.right_pane,
                                         text=labels['firstname'])
        self.firstname = ttk.Entry(self.right_pane, font=('Arial', 13))

        self.middlename_label = ttk.Label(self.right_pane,
                                          text=labels['middlename'])
        self.middlename = ttk.Entry(self.right_pane, font=('Arial', 13))

        # edit region
        self.region_label = ttk.Label(self.right_pane, text=labels['region'])
        self.region_edit = tk.Text(
            self.right_pane, height=2, width=35, bd=1, font=('Arial', 13),
            highlightcolor='#6fa8d8', wrap='word',
            highlightbackground='#bcbcbc')
        self.region_type = tk.IntVar()
        self.region0 = ttk.Radiobutton(
            self.right_pane, value=0, variable=self.region_type,
            text=labels['region0'], command=self.check_regtype)
        self.region1 = ttk.Radiobutton(
            self.right_pane, value=1, variable=self.region_type,
            command=self.check_regtype,
            text=labels['error_region1'].strip(' :.'))
        self.region2 = ttk.Radiobutton(
            self.right_pane, value=2, variable=self.region_type,
            command=self.check_regtype,
            text=labels['error_region2'].strip(' :.'))
        self.region3 = ttk.Radiobutton(
            self.right_pane, value=3, variable=self.region_type,
            command=self.check_regtype,
            text=labels['error_region3'].strip(' :.'))

        # common buttons
        self.save_button = ttk.Button(
            self.right_pane, text=labels['save'], width=15)
        self.cancel_button = ttk.Button(
            self.right_pane, text=labels['cancel'], width=15)
        self.delete_button = ttk.Button(
            self.right_pane, text=labels['delete'], width=20)

    #################################################################
    # methods displaying appropriate widgets
    #################################################################

    def open_user_pane(self):
        """
        Opens right pane to add or edit user
        """
        # first clear everything
        self.cancel_edit()
        self.username_edit.delete(0, 'end')
        self.email.delete(0, 'end')
        self.user_signature.delete('1.0', 'end')
        self.warning_area['text'] = ''

        # removes selection on the left pane
        self.cf_directors.set('')
        self.region.set('')

        # display labels
        self.right_pane.grid(row=0, column=3, columnspan=2, rowspan=5,
                             sticky='wn', padx=10, pady=10)
        self.username_edit_label.grid(
            row=0, column=0, sticky='en', pady=5, padx=2)
        self.username_edit.grid(
            row=0, column=1, pady=5, columnspan=2, sticky='news')

        self.email_label.grid(row=1, column=0, padx=2, pady=5,
                              sticky='en')
        self.email.grid(row=1, column=1, columnspan=2, pady=5,
                        sticky='news')

        self.user_signature_label.grid(
            row=2, column=0, pady=5, padx=2, sticky='en')
        self.user_signature.grid(row=2, column=1, pady=5, sticky='news')
        self.scroll_signature.grid(row=2, column=2, pady=5, sticky='nes')

        # display buttons
        self.save_button.grid(row=3, column=0, pady=20, padx=50,
                              columnspan=3, sticky='nw')
        self.cancel_button.grid(row=3, column=0, columnspan=3, padx=50,
                                pady=20, sticky='en')

        # enable button commands
        self.cancel_button['command'] = self.cancel_edit

    def edit_user_pane(self):
        """
        Opens 'Edit user' pane
        """
        self.open_user_pane()

        # check if empty choice to abort
        if not self.username.get():
            self.cancel_edit()
            self.warning_area['text'] += labels['no_user_edit']
            return

        # store current username
        users.current = self.username.get()

        # add right pane label
        self.right_pane['text'] = labels['edit_user_pane']

        # insert data
        self.username_edit.insert(0, users.current)
        self.email.insert(0, users[users.current].email)
        self.user_signature.insert('1.0', users[users.current].signature)

        # display 'Delete' button
        self.delete_button.grid(row=4, column=0, pady=10,
                                columnspan=3, sticky='n')

        # apply 'Save' button command
        self.save_button['command'] = self.edit_user
        self.delete_button['command'] = self.delete_user

    def add_user_pane(self):
        """
        Opens up the form to add a new user
        """
        self.open_user_pane()

        # removes selection on the left pane
        self.username.set('')
        users.current = None

        # add right pane label
        self.right_pane['text'] = labels['add_user_pane']

        # apply 'Save' button command
        self.save_button['command'] = self.add_user

    def open_dept_pane(self):
        """
        Opens 'Edit CF directors' pane
        """
        # first clear everything
        self.cancel_edit()
        self.lastname.delete(0, 'end')
        self.firstname.delete(0, 'end')
        self.middlename.delete(0, 'end')
        self.email.delete(0, 'end')
        self.warning_area['text'] = ''

        # removes selection on the left pane
        self.username.set('')
        self.region.set('')

        # check if empty choice to abort
        if not self.cf_directors.get():
            self.cancel_edit()
            self.warning_area['text'] += labels['no_dir_edit']
            return

        # remember dept name
        dept.current = self.cf_directors.get()

        # set right pane label
        self.right_pane['text'] = labels['edit_dept']

        # display evth
        self.right_pane.grid(row=0, column=3, columnspan=2, rowspan=5,
                             sticky='wn', padx=10, pady=10)
        self.lastname_label.grid(row=0, column=0, sticky='en', pady=5,
                                 padx=2)
        self.lastname.grid(row=0, column=1, sticky='news', pady=5, padx=2)
        self.firstname_label.grid(row=1, column=0, sticky='en', pady=5,
                                  padx=2)
        self.firstname.grid(row=1, column=1, sticky='news', pady=5, padx=2)
        self.middlename_label.grid(row=2, column=0, sticky='en', pady=5,
                                   padx=2)
        self.middlename.grid(row=2, column=1, sticky='news', pady=5, padx=2)
        self.email_label.grid(row=3, column=0, sticky='en', pady=5, padx=2)
        self.email.grid(row=3, column=1, sticky='news', pady=5, padx=2)

        # insert data
        self.lastname.insert(0, dept[dept.current].lastname)
        self.firstname.insert(0, dept[dept.current].firstname)
        self.middlename.insert(0, dept[dept.current].middlename)
        self.email.insert(0, dept[dept.current].email)

        # display buttons
        self.save_button.grid(row=4, column=0, pady=20, padx=50,
                              columnspan=2, sticky='nw')
        self.cancel_button.grid(row=4, column=0, columnspan=2, padx=50,
                                pady=20, sticky='en')

        # enable button commands
        self.save_button['command'] = self.edit_dept
        self.cancel_button['command'] = self.cancel_edit

    def open_region_pane(self):
        """
        Opens up a form to edit/add region
        """
        # first clear everything
        self.cancel_edit()
        self.region_edit.delete('1.0', 'end')
        self.lastname.delete(0, 'end')
        self.firstname.delete(0, 'end')
        self.middlename.delete(0, 'end')
        self.email.delete(0, 'end')
        self.warning_area['text'] = ''

        # removes selection on the left pane
        self.cf_directors.set('')
        self.username.set('')

        # display labels
        self.right_pane.grid(row=0, column=3, columnspan=2, rowspan=5,
                             sticky='wn', padx=10, pady=10)
        self.region_label.grid(row=0, column=0, sticky='en', pady=5, padx=2)
        self.region_edit.grid(row=0, column=1, sticky='news', pady=5)

        self.region0.grid(row=1, column=1, sticky='wn', padx=10)
        self.region1.grid(row=2, column=1, sticky='wn', padx=10)
        self.region2.grid(row=3, column=1, sticky='wn', padx=10)
        self.region3.grid(row=4, column=1, sticky='wn', padx=10)

        self.lastname_label.grid(row=5, column=0, sticky='en', pady=5, padx=2)
        self.lastname.grid(row=5, column=1, sticky='news', pady=5)
        self.firstname_label.grid(row=6, column=0, sticky='en', pady=5, padx=2)
        self.firstname.grid(row=6, column=1, sticky='news', pady=5)
        self.middlename_label.grid(row=7, column=0, sticky='en', pady=5,
                                   padx=2)
        self.middlename.grid(row=7, column=1, sticky='news', pady=5, padx=2)
        self.email_label.grid(row=8, column=0, sticky='en', pady=5, padx=2)
        self.email.grid(row=8, column=1, sticky='news', pady=5)

        # display buttons
        self.save_button.grid(row=9, column=0, pady=20, padx=50,
                              columnspan=3, sticky='nw')
        self.cancel_button.grid(row=9, column=0, columnspan=3, padx=50,
                                pady=20, sticky='en')

        # enable button commands
        self.cancel_button['command'] = self.cancel_edit

    def edit_region_pane(self):
        """
        Opens the right pane to edit region's info
        """
        self.open_region_pane()

        # check if empty choice to abort
        if not self.region.get():
            self.cancel_edit()
            self.warning_area['text'] += labels['no_region_edit']
            return

        # store current region
        regions.current = self.region.get()

        # add right pane label
        self.right_pane['text'] = labels['edit_region_pane']

        # insert data
        self.region_edit.insert('1.0', regions.current)
        # check region code to proceed with insertion
        if regions[regions.current].regtype == 1:
            self.region1.invoke()
        elif regions[regions.current].regtype == 2:
            self.region2.invoke()
        elif regions[regions.current].regtype == 3:
            self.region3.invoke()
        else:
            self.region0.invoke()
            self.lastname.insert(0, regions[regions.current].lastname)
            self.firstname.insert(0, regions[regions.current].firstname)
            self.middlename.insert(0, regions[regions.current].middlename)
            self.email.insert(0, regions[regions.current].email)

        # display 'Delete' button
        self.delete_button.grid(row=10, column=0, pady=10,
                                columnspan=3, sticky='n')

        # apply 'Save' button command
        self.save_button['command'] = self.edit_region
        self.delete_button['command'] = self.delete_region

    def add_region_pane(self):
        """
        Opens up a form to add a new region, shows warning message
        """
        self.open_region_pane()

        # displays a warning about subjects of the Federation
        self.warning_area['text'] = labels['add_region_confirm']

        # sets radiobutton to region0 position
        self.region0.invoke()

        # removes selection on the left pane
        self.region.set('')
        regions.current = None

        # add right pane label
        self.right_pane['text'] = labels['add_region_pane']

        # apply 'Save' button command
        self.save_button['command'] = self.add_region

    #################################################################
    # methods accomplishing appropriate logic (save, delete, etc.)
    #################################################################

    def update_user(self, userkey, warn_msg, end_msg):
        """
        Validates input and updates the selected user.
        Used in edit_user and add_user
        """
        self.warning_area['text'] = ''
        usermail = self.email.get().strip(' \t\n')
        usersign = self.user_signature.get('1.0', 'end-1c').strip()

        # check for empty fields
        if not (userkey and usermail and usersign):
            self.warning_area['text'] = labels['empty_fields']
            if not userkey:
                self._prev = None
            return

        # if consecutive click and name is not changed again
        if userkey == self._prev:
            users.force_update(User, userkey, usermail, usersign)
            self._prev = None
        # if any other click
        else:
            try:
                users.update_item(User, userkey, usermail, usersign)
                self._prev = None
            except AssertionError:
                # show warning
                self.warning_area['text'] = warn_msg
                # store the suggested name
                self._prev = userkey
                return

        # inform that evth is done
        self.warning_area['text'] = end_msg

    @logic_decorator('users')
    def edit_user(self):
        """
        Edit user
        """
        userkey = self.username_edit.get().strip(' \t\n')
        self.update_user(
            userkey,
            labels['user_duplicate'].format(userkey, users.current),
            labels['user_updated'].format(userkey))

        if self._prev is None and userkey != '':
            users.current = userkey
            self._clicked = False
            # update left pane Combobox
            self.username.configure(values=users.keys())
            self.username.set(userkey)

    @logic_decorator('users')
    def add_user(self):
        """
        Adds a new user
        """
        userkey = self.username_edit.get().strip(' \t\n')
        self.update_user(
            userkey, labels['user_exists'].format(userkey),
            labels['user_added'].format(userkey))

    @logic_decorator('users')
    def delete_user(self):
        """
        Deletes a user
        """
        # ask for confirmation
        if not self._clicked:
            self.warning_area['text'] = labels['confirm_user_delete'].format(
                users.current)
            self._clicked = True
        # delete upon 2nd click, close the right pane, clear the left one
        else:
            del users[users.current]
            self.cancel_edit()
            self.warning_area['text'] = labels['user_deleted'].format(
                users.current)
            self.username.set('')

    @logic_decorator('dept')
    def edit_dept(self):
        """
        Validates and saves info on CF directors
        """
        # initial values
        lastname = self.lastname.get().strip(' \n\t')
        firstname = self.firstname.get().strip(' \n\t')
        middlename = self.middlename.get().strip(' \n\t')
        dir_email = self.email.get().strip(' \n\t')

        # update dept dictionary
        dept.update_item(Department, dept.current, firstname, middlename,
                         lastname, dir_email)

        # inform of saving
        self.warning_area['text'] = labels['dir_updated'].format(
            dept.current)

    def update_region(self, regkey, warn_msg, end_msg, warn2, warn3):
        """
        Validates input and updates the selected region.
        Used in edit_region and add_region
        """
        self.warning_area['text'] = ''
        regtype = self.region_type.get()

        # if region code is not 0 other values should be None
        if regtype > 0:
            firstname, middlename, lastname, regmail = None, None, None, None
        else:
            firstname = self.firstname.get().strip(' \n\t')
            middlename = self.middlename.get().strip(' \n\t')
            lastname = self.lastname.get().strip(' \t\n')
            regmail = self.email.get().strip(' \t\n')

        # check for empty fields
        if (not regkey and regtype) or \
               (not regtype and not (regkey and firstname and middlename
                                     and lastname and regmail)):
            #show warning
            self.warning_area['text'] = labels['empty_fields']
            # to reset previous_name for edit section
            if not regkey:
                self._prev = None
            return

        # if consecutive click and name is not changed again
        if regkey == self._prev:
            regions.force_update(Region, regkey, regtype, firstname,
                                 middlename, lastname, regmail)
            self._prev = None
        # if any other click
        else:
            try:
                regions.update_item(Region, regkey, regtype, firstname,
                                    middlename, lastname, regmail)
                self._prev = None
            except AssertionError:
                if regkey in regions:
                    # if region exists
                    self.warning_area['text'] = warn_msg
                else:
                    # confirm that the region name is not changed accidentally
                    self.warning_area['text'] = warn2
                    self.warning_area['text'] += warn3
                # store the suggested name
                self._prev = regkey
                return

        # inform that evth is done
        self.warning_area['text'] = end_msg

    @logic_decorator('regions')
    def edit_region(self):
        """
        Validate and save changes to a region upon 'Save' click
        """
        regkey = self.region_edit.get('1.0', 'end-1c').strip(' \t\n')
        self.update_region(
            regkey,
            labels['region_duplicate'].format(regkey, regions.current),
            labels['region_updated'].format(regkey),
            labels['amend_regname_confirm'].format(regions.current),
            labels['add_region_confirm'])

        if self._prev is None and regkey != '':
            regions.current = regkey
            self._clicked = False
            # update left pane Combobox
            self.region.configure(values=regions.keys())
            self.region.set(regkey)

    @logic_decorator('regions')
    def delete_region(self):
        """
        Delets a region upon confirmation
        """
        # ask for confirmation
        if not self._clicked:
            self.warning_area['text'] = labels['confirm_reg_delete'].format(
                regions.current)
            self._clicked = True
        # delete upon 2nd click, close the right pane, clear the left one
        else:
            del regions[regions.current]
            self.cancel_edit()
            self.warning_area['text'] = labels['region_deleted'].format(
                regions.current)
            self.region.set('')

    @logic_decorator('regions')
    def add_region(self):
        """
        Validates and adds a new region upon 'Save' click
        """
        regkey = self.region_edit.get('1.0', 'end-1c').strip(' \t\n')
        self.update_region(
            regkey,
            labels['region_exists'].format(regkey),
            labels['region_added'].format(regkey),
            labels['add_region_confirm'],
            labels['click_to_confirm'])

    def check_regtype(self):
        """
        Checks region type and disables lastname, firstname and email
        fields of the edit/add region pane if the region type is not 0.
        Otherwise the fields are enabled back.
        """
        if self.region_type.get() > 0:
            self.firstname.configure(state='disabled')
            self.middlename.configure(state='disabled')
            self.lastname.configure(state='disabled')
            self.email.configure(state='disabled')
        else:
            self.firstname.configure(state='normal')
            self.middlename.configure(state='normal')
            self.lastname.configure(state='normal')
            self.email.configure(state='normal')

    def cancel_edit(self):
        """
        Cancels editing data (when 'Cancel' button is clicked).
        Hides the right pane, no changes are saved.
        Dismisses previous states if any.
        """
        for widg in self.right_pane.winfo_children():
            # this part is needed to restore evth after moving radiobutton
            # in edit/add region section because the same widgets are used
            # in dept section as well
            try:
                widg.configure(state='normal')
            except tk.TclError:
                pass
            finally:
                # hides all widgets of the right pane
                widg.grid_remove()
        self.right_pane.grid_remove()
        self.warning_area['text'] = ''
        self._clicked = False
        self._prev = None
