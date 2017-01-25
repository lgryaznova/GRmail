"""
GRmail ver.1.1
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fdialog
from datetime import datetime, timedelta, date
import pickle
import os
import sys
import re

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    Amended. Original from http://stackoverflow.com/a/13790741
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.realpath(__file__))

    return os.path.join(base_path, relative_path)


def process_region(region_name):
    """
    Helper function to shorten region's names (exclude parentheses)
    text (string), region's name with parentheses

    Returns short region's name without parentheses
    """
    pattern1 = re.compile('.+[(].*[)]$')
    pattern2 = re.compile('.+ '+chr(8212)+' .*$')

    if pattern2.search(region_name):
        return region_name.split(' '+chr(8212)+' ')[0]
    elif pattern1.search(region_name):
        return region_name.split(' (')[0]
    else:
        return region_name


def logic_decorator(option):
    """
    Updates pickle files given the filename as option to the decorator
    (accepts 'users', 'dept', or 'regions')
    """
    def the_decorator(func):
        """ The decorator itself """
        def wrapper(self, *args, **kwargs):
            """ Updates pickle files """
            func(self, *args, **kwargs)
            try:
                with open(resource_path(option + '.pkl'), 'wb') as tempfile:
                    pickle.dump(globals()[option], tempfile)
            except KeyError:
                print('Wrong decorator option, check the code')
                raise
        return wrapper
    return the_decorator


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
        self.nametowidget(widget_name)['values'] = sorted(new_list)
        try:
            self.nametowidget(widget_name).set_completion_list(new_list)
        except AttributeError:
            return


class MainWindow(StandardTab):
    """
    First tab: main window of the app
    """
    def create_widgets(self):
        """
        Create all widgets
        """
        ############################################################
        # LEFT PANE
        ############################################################
        # fill in form
        self.left_pane = ttk.LabelFrame(self, text=labels['left_pane'],
                                        width=30)
        self.left_pane.grid(row=0, column=0, columnspan=2, rowspan=10,
                            sticky='news', padx=10, pady=10)

        # choose user
        self.username_label = ttk.Label(self.left_pane,
                                        text=labels['username'])
        self.username_label.grid(row=0, column=0, sticky='en', pady=2, padx=2)
        self.username = ttk.Combobox(
            self.left_pane, values=sorted(users.keys()), state='readonly',
            font=('Arial', 13), postcommand=lambda: self.update_list(
                str(self.username), users.keys()))
        self.username.grid(row=0, column=1, sticky='news', pady=2)

        # FWD to legal
        self.legal_fwd = tk.IntVar()
        self.legal_fwd_cb = ttk.Checkbutton(
            self.left_pane, text=labels['legal_fwd'],
            variable=self.legal_fwd, onvalue=1, offvalue=0,
            command=self.legal_forward)
        self.legal_fwd_cb.grid(row=1, column=1, sticky='w', pady=2)

        # inform legal
        self.legal_cc = tk.IntVar()
        self.legal_cc_cb = ttk.Checkbutton(
            self.left_pane, text=labels['legal_cc'],
            variable=self.legal_cc, onvalue=1, offvalue=0)
        self.legal_cc_cb.grid(row=2, column=1, sticky='w', pady=2)

        # cc to GR director
        self.gr_cc = tk.IntVar()
        self.gr_cc.set(1)
        self.gr_cc_cb = ttk.Checkbutton(
            self.left_pane, text=labels['gr_cc'],
            variable=self.gr_cc, onvalue=1, offvalue=0)
        self.gr_cc_cb.grid(row=3, column=1, sticky='w', pady=2)

        # enter customer's name
        self.customer_label = ttk.Label(self.left_pane,
                                        text=labels['customer'])
        self.customer_label.grid(row=4, column=0, sticky='en', pady=2, padx=2)
        self.customer = ttk.Entry(self.left_pane, font=('Arial', 13))
        self.customer.grid(row=4, column=1, sticky='news', pady=2)

        # enter region
        self.region_label = ttk.Label(self.left_pane, text=labels['region'])
        self.region_label.grid(row=5, column=0, sticky='en', pady=2, padx=2)
        self.region = AutocompleteCombobox(
            self.left_pane, font=('Arial', 13),
            postcommand=lambda: self.update_list(str(self.region),
                                                 regions.keys()))
        self.region.set_completion_list(list(regions.keys()))
        self.region.bind("<Return>", self.focus_next_window)
        self.region.grid(row=5, column=1, sticky='news', pady=2)

        # enter deadline
        self.deadline_label = ttk.Label(self.left_pane,
                                        text=labels['deadline'])
        self.deadline_label.grid(row=6, column=0, sticky='e', pady=2, padx=2)
        self.deadline = ttk.Entry(self.left_pane, font=('Arial', 13))
        self.deadline.grid(row=6, column=1, sticky='news', pady=2)

        # enter reason
        self.reason_label = ttk.Label(self.left_pane, text=labels['reason'])
        self.reason_label.grid(row=7, column=0, sticky='en', pady=2, padx=2)
        self.reason = tk.Text(self.left_pane, height=2, width=30, bd=1,
                              highlightcolor='#6fa8d8', font=('Arial', 13),
                              wrap='word', highlightbackground='#bcbcbc')
        self.reason.grid(row=7, column=1, sticky='news', pady=2)

        # enclose attachment
        self.attach_flag = tk.IntVar()
        self.attach_cb = ttk.Checkbutton(
            self.left_pane, text=labels['attachment'],
            variable=self.attach_flag, onvalue=1, offvalue=0,
            command=self.check_attachment)
        self.attach_cb.grid(row=8, column=0, sticky='en', pady=2, padx=2)
        self.attach = tk.StringVar()
        self.attach_name = ttk.Label(self.left_pane, text=labels['no_files'],
                                     justify='left', style='Attachment.TLabel')
        self.attach_name.grid(row=8, column=1, sticky='w', pady=2)
        self.browse_button = ttk.Button(self.left_pane, text=labels['browse'],
                                        command=self.show_attachment)
        self.browse_button.grid(row=8, column=1, sticky='en', pady=2)

        # place to display error messages if any
        self.errors = ttk.Label(self.left_pane, font=('Arial', 13, 'bold'),
                                foreground='red', wraplength=400)
        self.errors['text'] = '\n'
        self.errors.grid(row=9, column=0, columnspan=2, pady=10)

        # generate text button
        self.generate_button = ttk.Button(
            self.left_pane, text=labels['generate'],
            style='Generate.TButton', command=self.check_input)
        self.generate_button.grid(row=10, column=0, columnspan=2, pady=2)

        ############################################################
        # RIGHT PANE
        ############################################################
        # letter section
        self.right_pane = ttk.LabelFrame(self, text=labels['right_pane'])
        self.right_pane.grid(row=0, column=2, columnspan=3, rowspan=12,
                             sticky='wn', padx=10, pady=10)

        # To:
        self.to_label = ttk.Label(self.right_pane, text=labels['to'])
        self.to_label.grid(row=0, column=2, sticky='en', pady=2, padx=2)
        self.addr_to = ttk.Entry(self.right_pane, font=('Arial', 11))
        self.addr_to.grid(row=0, column=3, columnspan=2, sticky='news', pady=2)

        # CC:
        self.cc_label = ttk.Label(self.right_pane, text=labels['cc'])
        self.cc_label.grid(row=1, column=2, sticky='en', pady=2, padx=2)
        self.addr_cc = ttk.Entry(self.right_pane, font=('Arial', 11))
        self.addr_cc.grid(row=1, column=3, columnspan=2, sticky='news', pady=2)

        # Subj:
        self.subj_label = ttk.Label(self.right_pane, text=labels['subject'])
        self.subj_label.grid(row=2, column=2, sticky='en', pady=2, padx=2)
        self.subj = tk.Text(self.right_pane, height=2, width=40, bd=1,
                            highlightcolor='#6fa8d8', font=('Arial', 11),
                            wrap='word', highlightbackground='#bcbcbc')
        self.subj.grid(row=2, column=3, rowspan=2, columnspan=2,
                       sticky='news', pady=2)

        # body:
        self.body = tk.Text(self.right_pane, height=15, width=50, bd=1,
                            highlightcolor='#6fa8d8', font=('Arial', 11),
                            wrap='word', highlightbackground='#bcbcbc')
        self.body.grid(row=4, column=2, columnspan=2, rowspan=7,
                       sticky='news', pady=2)
        self.scroll_body = ttk.Scrollbar(self.right_pane)
        self.scroll_body.grid(row=4, column=4, rowspan=7, pady=2, sticky='nes')
        self.scroll_body['command'] = self.body.yview
        self.body['yscrollcommand'] = self.scroll_body.set

        # send button
        self.send_button = ttk.Button(
            self.right_pane, text=labels['send'], command=self.send)
        self.send_button.grid(
            row=12, column=2, columnspan=3, sticky='w', pady=2, padx=70)

        # quit button
        self.quit = ttk.Button(self.right_pane, text=labels['exit'],
                               command=root.destroy)
        self.quit.grid(row=12, column=2, columnspan=3, pady=2, padx=70,
                       sticky='e')

    def legal_forward(self):
        """
        Disables fields which are not necessary for legal dept letters
        or sets the defaults otherwise.
        """
        if self.legal_fwd.get():
            self.deadline.configure(state='disabled')
            self.region.configure(state='disabled')
            self.legal_cc_cb.configure(state='disabled')
        else:
            self.deadline.configure(state='normal')
            self.region.configure(state='normal')
            self.legal_cc_cb.configure(state='normal')

    def check_attachment(self):
        """
        Activates when the attachment checkbutton is toggled, checks
        its state.
        'On' state means there will be attachments, opens up file
        dialog and proceed accordingly (see self.get_attachment).
        'Off' state means no attachment, so we reset the variable
        holding paths to attachments (self.attach) to default and
        display standard text instead of filenames of attachments.
        """
        if not self.attach_flag.get():
            self.attach = tk.StringVar()
            self.attach_name['text'] = labels['no_files']
        else:
            self.show_attachment()

    def show_attachment(self):
        """
        Stores a tuple with full paths to selected attachments
        in self.attach. Displays filenames of selected attachments
        in the appropriate field (or default message if nothing
        selected). Toggles the attachment checkbutton to visualize
        if there are selected attachments and to make it easy
        to remove them if necessary.
        """
        self.attach = fdialog.askopenfilenames()

        # update interface in accordance with (de)selected attachments
        # (checkbutton and displayed filenames or default text)
        if len(self.attach) != 0:
            # get filenames to display in app
            filenames = []
            for i in self.attach:
                filenames.append(i.split('/')[-1])
            self.attach_name['text'] = ',\n'.join(filenames)
            self.attach_flag.set(1)
        else:
            self.attach_name['text'] = labels['error_no_attachment']
            self.attach_flag.set(0)

    def process_date(self, textdate):
        """
        Tries to convert deadline from user input into datetime object.
        If fails, updates error field

        text (string), input by user (date is expected)
        Returns datetime object if input is valid and None otherwise
        """
        # no check if empty line or to be forwarded to legal function
        if self.deadline.get().strip() == '' or self.legal_fwd.get() == 1:
            return None

        converted = None

        # tries to convert into datetime object
        for fmt in ('%d-%m-%Y', '%d-%m-%y', '%d.%m.%Y', '%d.%m.%y',
                    '%d/%m/%Y', '%d/%m/%y'):
            try:
                converted = datetime.strptime(textdate, fmt).date()
            except ValueError:
                pass

        # in case of error update error field
        if converted is None:
            self.errors['text'] += labels['error_recognise_date']
            self.deadline_label.configure(style='Red.TLabel')
        # otherwise check if it's not the past date
        elif converted < date.today():
            self.errors['text'] += labels['error_early_deadline']
            self.deadline_label.configure(style='Red.TLabel')
            converted = None

        return converted

    def check_input(self):
        """
        Checks if user entered all the necessary info.

        Invokes generate_letter() if input is OK
        and displays errors otherwise.
        """
        # set initial state
        flag = True
        attach_flag = True
        self.username_label.configure(style='TLabel')
        self.customer_label.configure(style='TLabel')
        self.region_label.configure(style='TLabel')
        self.reason_label.configure(style='TLabel')
        self.deadline_label.configure(style='TLabel')
        self.attach_name.configure(style='Attachment.TLabel')
        self.errors['text'] = '\n'
        self.addr_to.configure(state='normal')
        self.addr_cc.configure(state='normal')
        self.subj.configure(state='normal')
        self.body.configure(state='normal')
        self.send_button.configure(state='normal')

        # if not to be forwarded to legal function:
        if not self.legal_fwd.get():
            # check region
            if self.region.get() == '':
                self.region_label.configure(style='Red.TLabel')
                flag = False
            # only non-problem regions are processed
            elif regions[self.region.get()][0]:
                # update error field
                if regions[self.region.get()][0] == 1:
                    self.errors['text'] = (process_region(self.region.get())
                                           + labels['error_region1'])
                elif regions[self.region.get()][0] == 2:
                    self.errors['text'] = (process_region(self.region.get())
                                           + labels['error_region2'])
                elif regions[self.region.get()][0] == 3:
                    self.errors['text'] = (process_region(self.region.get())
                                           + labels['error_region3'])
                self.errors['text'] += labels['error_manual_processing']

                # disable letter fields to prevent sending
                self.addr_to.configure(state='disabled')
                self.addr_cc.configure(state='disabled')
                self.subj.configure(state='disabled')
                self.body.configure(state='disabled')
                self.send_button.configure(state='disabled')
                # break out
                return

        # check username
        if self.username.get().strip() == '':
            self.username_label.configure(style='Red.TLabel')
            flag = False
        # check customer's name
        if self.customer.get().strip() == '':
            self.customer_label.configure(style='Red.TLabel')
            flag = False
        # # check attachments
        # if not isinstance(self.attach, tuple):
        #     self.errors['text'] += labels['error_no_attachment']
        #     self.attach_name.configure(style='Red.TLabel')
        #     attach_flag = False
        # check reasonning
        if self.reason.get('1.0', 'end').strip() == '':
            self.reason_label.configure(style='Red.TLabel')
            flag = False

        # update error message field
        if not flag:
            self.errors['text'] += labels['error_empty_field']

        # if check is passed, generate a letter
        if flag and attach_flag:
            self.generate_letter()

    def generate_letter(self):
        """
        Returns a new letter instead of the old one (string)
        """
        # FIRST clear everything
        self.addr_to.delete(0, 'end')
        self.addr_cc.delete(0, 'end')
        self.subj.delete('1.0', 'end')
        self.body.delete('1.0', 'end')

        # helper function to get due date for regions
        def get_duedate(deadline):
            """
            Helper function to get due date out of the letter's
            deadline (for regions)

            deadline (datetime.date), deadline from the letter
            Returns duedate (datetime.date)
            """
            # if deadline is in 6+ days
            if (deadline-date.today()).days >= 6:
                # set due date 2 days before the deadline
                # or earlier if weekend
                if (deadline-timedelta(2)).weekday() < 5:
                    return deadline-timedelta(2)
                else:
                    return deadline-timedelta(4)
            # if deadline within 6 days from today
            else:
            # make a list of business days within this period
                businessdays = [deadline-timedelta(x) for x in \
                                range((deadline-date.today()).days+1) \
                                if (deadline-timedelta(x)).weekday() < 5]
            # if there are 5 business days set due date 2 days before
                if len(businessdays) == 5:
                    return businessdays[2]
            # if there are 3 or 4 days set due date 1 day before deadline
                elif len(businessdays) >= 3:
                    return businessdays[1]
            # otherwise set deadline as duedate
                else:
                    return businessdays[0]

        def get_dirname(fullname):
            """
            Takes director's full name and returns either firstname or
            firstname and middle name (used in Russian) depending on
            the user settings.

            fullname, list - list of strings representing full name
            Returns a string of one or two words
            """
            if address_book.use_middlename.get():
                return ' '.join(fullname[1:])
            else:
                return fullname[1]


        # assign user input values to local variables
        region = process_region(self.region.get())
        customer = self.customer.get().strip()
        reasoning = self.reason.get('1.0', 'end-1c').strip()
        signature = users[self.username.get()][1]

        # assign director name and update headers: TO
        if self.legal_fwd.get():
            self.addr_to.insert(0, dept['legal'][1])
            director = get_dirname(dept['legal'][0].split())
        else:
            self.addr_to.insert(0, regions[self.region.get()][2])
            director = get_dirname(regions[self.region.get()][1].split())

        # update headers: CC
        if self.gr_cc.get():
            self.addr_cc.insert(0, dept['gr'][1])
        if self.legal_cc.get():
            self.addr_cc.insert('end', '; '+dept['legal'][1])

        # update headers: SUBJ
        if self.region.get() == '':
            subject = text['subjText'].format(customer, reasoning)
        else:
            subject = text['subjTextRegion'].format(customer, region, reasoning)

        # append due date if any
        deadline = self.process_date(self.deadline.get())
        if deadline:
            duedate = get_duedate(deadline)
            subject = (text['due'].format(datetime.strftime(duedate, '%d.%m'))
                       + subject)

        self.subj.insert('1.0', subject)

        # body
        if self.legal_fwd.get():
            body_text = text['legalReply'].format(
                director, customer, reasoning, signature)
        elif self.legal_cc.get():
            body_text = text['regionLegalReply'].format(
                director, customer, region, reasoning, signature)
        elif deadline:
            body_text = text['ourReply'].format(
                director, customer, region, reasoning,
                datetime.strftime(duedate, '%d.%m.%Y'), signature)
        else:
            body_text = text['regionReply'].format(
                director, customer, region, reasoning, signature)

        self.body.insert('1.0', body_text)

    def send(self):
        """
        Not yet implemented. Copies body of the letter instead.
        """
        root.clipboard_clear()
        root.clipboard_append(self.subj.get('1.0', 'end-1c') + '\n\n'
                              + self.body.get('1.0', 'end-1c'))


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
        self._clicked_upd = False
        self._clicked_del = False
        self._clicked_add = False
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
            self.left_pane, values=sorted(users.keys()),
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
            self.left_pane, values=sorted(x.upper() for x in dept.keys()),
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
        self.region.set_completion_list(list(regions.keys()))
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

        # use middlename
        self.use_middlename = tk.IntVar()
        self.use_middlename.set(1)
        self.middlename_cb = ttk.Checkbutton(
            self.left_pane, text=labels['use_middlename'],
            variable=self.use_middlename, onvalue=1, offvalue=0)
        self.middlename_cb.grid(row=5, column=1, pady=5, sticky='nw')

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
        self.lastname = ttk.Entry(self.right_pane, font=('Arial', 13))

        self.firstname_label = ttk.Label(self.right_pane,
                                         text=labels['firstname'])
        self.firstname = tk.Text(
            self.right_pane, height=2, width=35, bd=1,
            highlightcolor='#6fa8d8', font=('Arial', 13), wrap='word',
            highlightbackground='#bcbcbc')

        # edit region
        self.region_label = ttk.Label(self.right_pane, text=labels['region'])
        self.region_edit = tk.Text(
            self.right_pane, height=2, width=35, bd=1, font=('Arial', 13),
            highlightcolor='#6fa8d8', wrap='word',
            highlightbackground='#bcbcbc')
        self.region_code = tk.IntVar()
        self.region0 = ttk.Radiobutton(
            self.right_pane, value=0, variable=self.region_code,
            text=labels['region0'], command=self.check_reg_code)
        self.region1 = ttk.Radiobutton(
            self.right_pane, value=1, variable=self.region_code,
            command=self.check_reg_code,
            text=labels['error_region1'].strip(' :.'))
        self.region2 = ttk.Radiobutton(
            self.right_pane, value=2, variable=self.region_code,
            command=self.check_reg_code,
            text=labels['error_region2'].strip(' :.'))
        self.region3 = ttk.Radiobutton(
            self.right_pane, value=3, variable=self.region_code,
            command=self.check_reg_code,
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
        self._user_current = self.username.get()

        # add right pane label
        self.right_pane['text'] = labels['edit_user_pane']

        # insert data
        self.username_edit.insert(0, self.username.get())
        self.email.insert(0, users[self.username.get()][0])
        self.user_signature.insert('1.0', users[self.username.get()][1])

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
        self.firstname.delete('1.0', 'end')
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
        self._cf_func = self.cf_directors.get().lower()

        # initial values
        dir_lastname = dept[self._cf_func][0].split()[0]
        dir_firstname = ' '.join(dept[self._cf_func][0].split()[1:])
        dir_email = dept[self._cf_func][1]

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
        self.email_label.grid(row=2, column=0, sticky='en', pady=5, padx=2)
        self.email.grid(row=2, column=1, sticky='news', pady=5, padx=2)

        # insert data
        self.lastname.insert(0, dir_lastname)
        self.firstname.insert('1.0', dir_firstname)
        self.email.insert(0, dir_email)

        # display buttons
        self.save_button.grid(row=3, column=0, pady=20, padx=50,
                              columnspan=2, sticky='nw')
        self.cancel_button.grid(row=3, column=0, columnspan=2, padx=50,
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
        self.firstname.delete('1.0', 'end')
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
        self.email_label.grid(row=7, column=0, sticky='en', pady=5, padx=2)
        self.email.grid(row=7, column=1, sticky='news', pady=5)

        # display buttons
        self.save_button.grid(row=8, column=0, pady=20, padx=50,
                              columnspan=3, sticky='nw')
        self.cancel_button.grid(row=8, column=0, columnspan=3, padx=50,
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
        self._region_current = self.region.get()

        # add right pane label
        self.right_pane['text'] = labels['edit_region_pane']

        # insert data
        self.region_edit.insert('1.0', self._region_current)
        # check region code to proceed with insertion
        if regions[self._region_current][0] == 1:
            self.region1.invoke()
        elif regions[self._region_current][0] == 2:
            self.region2.invoke()
        elif regions[self._region_current][0] == 3:
            self.region3.invoke()
        else:
            self.region0.invoke()
            lastname = regions[self._region_current][1].split()[0]
            firstname = ' '.join(regions[self._region_current][1].split()[1:])
            reg_email = regions[self._region_current][2]
            self.lastname.insert(0, lastname)
            self.firstname.insert('1.0', firstname)
            self.email.insert(0, reg_email)

        # display 'Delete' button
        self.delete_button.grid(row=9, column=0, pady=10,
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

        # add right pane label
        self.right_pane['text'] = labels['add_region_pane']

        # apply 'Save' button command
        self.save_button['command'] = self.add_region

    #################################################################
    # methods accomplishing appropriate logic (save, delete, etc.)
    #################################################################

    @logic_decorator('users')
    def edit_user(self):
        """
        Validates input and saves changes to the selected user
        """
        self.warning_area['text'] = ''
        userkey = self.username_edit.get().strip(' \t\n')
        usermail = self.email.get().strip(' \t\n')
        usersign = self.user_signature.get('1.0', 'end-1c').strip()

        # check for empty fields
        if not (userkey and usermail and usersign):
            self.warning_area['text'] = labels['empty_fields']
            return

        # we may add email validation here, but since sending function
        # is not working yet, we postpone it for a while

        # if amended username is duplicate, request confirmation
        if (userkey != self._user_current
                and userkey in users
                and not self._clicked_upd):
            # show warning
            self.warning_area['text'] = labels['user_duplicate'].format(
                userkey, self._user_current)
            self._clicked_upd = True
            return

        # if username is not changed we update values only
        if userkey == self._user_current:
            users[userkey][0] = usermail
            users[userkey][1] = usersign
        # if username is new and unique, we update dictionary.
        # if username is duplicate, update upon we user confirmation
        elif userkey not in users or self._clicked_upd:
            users[userkey] = [usermail, usersign]
            del users[self._user_current]
            # update left pane Combobox
            self.username.configure(values=sorted(users.keys()))
            self.username.set(userkey)

        # reset flags and data
        self._user_current = userkey
        self._clicked_upd = False
        self._clicked_del = False

        # inform that evth is done
        self.warning_area['text'] = labels['user_updated'].format(userkey)

    @logic_decorator('users')
    def add_user(self):
        """
        Adds a new user after validation
        """
        self.warning_area['text'] = ''
        userkey = self.username_edit.get().strip(' \t\n')
        usermail = self.email.get().strip(' \t\n')
        usersign = self.user_signature.get('1.0', 'end-1c').strip()

        # check for empty fields
        if not (userkey and usermail and usersign):
            self.warning_area['text'] = labels['empty_fields']
            return

        # check if user exists
        if userkey in users and not self._clicked_add:
            self.warning_area['text'] = labels['user_exists'].format(userkey)
            self._clicked_add = True

        # add a new user to the dictionary
        elif self._clicked_add or userkey not in users:
            users[userkey] = [usermail, usersign]
            self.warning_area['text'] = labels['user_added'].format(userkey)

    @logic_decorator('users')
    def delete_user(self):
        """
        Deletes a user
        """
        # ask for confirmation
        if not self._clicked_del:
            self.warning_area['text'] = labels['confirm_user_delete'].format(
                self._user_current)
            self._clicked_del = True
        # delete upon 2nd click, close the right pane, clear the left one
        elif self._clicked_del:
            del users[self._user_current]
            self.warning_area['text'] = labels['user_deleted'].format(
                self._user_current)
            self._clicked_del = False
            self.username.set('')
            self.cancel_edit()

    @logic_decorator('dept')
    def edit_dept(self):
        """
        Validates and saves info on CF directors
        """
        # initial values
        lastname = self.lastname.get().strip(' \n\t')
        firstname = self.firstname.get('1.0', 'end-1c').strip(' \n\t')
        fullname = lastname + ' ' + firstname
        dir_email = self.email.get().strip(' \n\t')
        cf_func = self._cf_func

        # update dept dictionary
        dept[cf_func] = [fullname, dir_email]

        # inform of saving
        self.warning_area['text'] = labels['dir_updated'].format(
            cf_func.upper())

    @logic_decorator('regions')
    def edit_region(self):
        """
        Validate and save changes to a region upon 'Save' click
        """
        self.warning_area['text'] = ''
        regkey = self.region_edit.get('1.0', 'end-1c').strip(' \t\n')
        regcode = self.region_code.get()

        # if region code is not 0 other values should be None
        if regcode > 0:
            fullname, regmail = None, None
        else:
            fullname = (self.lastname.get().strip(' \t\n') + ' '
                        + self.firstname.get('1.0', 'end-1c').strip(' \n\t'))
            regmail = self.email.get().strip(' \t\n')

        # check for empty fields
        if (not regkey and regcode) or \
               (not regcode and not (regkey and fullname and regmail)):
            #show warning
            self.warning_area['text'] = labels['empty_fields']
            return

        # request confirmation to update region name
        if regkey != self._region_current and not self._clicked_upd:
            # if amended region name is duplicate, request confirmation
            if regkey in regions:
                self.warning_area['text'] = labels['region_duplicate'].format(
                    regkey, self._region_current)
            else:
                # confirmation that the region name is not changed accidentally
                self.warning_area['text'] = \
                    labels['amend_regname_confirm'].format(self._region_current)
                self.warning_area['text'] += labels['add_region_confirm']
            self._clicked_upd = True
            return

        # if region name is not changed we update values only
        if regkey == self._region_current:
            regions[regkey] = [regcode, fullname, regmail]
        # if username is new and unique, we update dictionary.
        # if username is duplicate, update upon we user confirmation
        elif self._clicked_upd:
            regions[regkey] = [regcode, fullname, regmail]
            del regions[self._region_current]
            # update left pane Combobox
            self.update_list(str(self.region), regions.keys())
            self.region.set(regkey)

        # reset flags and data
        self._region_current = regkey
        self._clicked_upd = False
        self._clicked_del = False

        # inform that evth is done
        self.warning_area['text'] = labels['region_updated'].format(regkey)

    @logic_decorator('regions')
    def delete_region(self):
        """
        Delets a region upon confirmation
        """
        # ask for confirmation
        if not self._clicked_del:
            self.warning_area['text'] = labels['confirm_reg_delete'].format(
                self._region_current)
            self._clicked_del = True
        # delete upon 2nd click, close the right pane, clear the left one
        elif self._clicked_del:
            del regions[self._region_current]
            self.warning_area['text'] = labels['region_deleted'].format(
                self._region_current)
            self._clicked_del = False
            self.region.set('')
            self.cancel_edit()

    @logic_decorator('regions')
    def add_region(self):
        """
        Validates and adds a new region upon 'Save' click
        """
        self.warning_area['text'] = ''
        regkey = self.region_edit.get('1.0', 'end-1c').strip(' \t\n')
        regcode = self.region_code.get()

        # if region code is not 0 other values should be None
        if regcode > 0:
            fullname, regmail = None, None
        else:
            fullname = (self.lastname.get().strip(' \t\n') + ' '
                        + self.firstname.get('1.0', 'end-1c').strip(' \n\t'))
            regmail = self.email.get().strip(' \t\n')

        # check for empty fields
        if (not regkey and regcode) or \
               (not regcode and not (regkey and fullname and regmail)):
            # display warning
            self.warning_area['text'] = labels['empty_fields']
            return

        # check if region exists
        if regkey in regions and not self._clicked_add:
            self.warning_area['text'] = labels['region_exists'].format(regkey)
            self._clicked_add = True

        # add a new user to the dictionary
        elif self._clicked_add or regkey not in regions:
            regions[regkey] = [regcode, fullname, regmail]
            self.warning_area['text'] = labels['region_added'].format(regkey)

    def check_reg_code(self):
        """
        Checks region code and disables lastname, firstname and email
        fields of the edit/add region pane if the region code is not 0.
        Otherwise the fields are enabled back.
        """
        if self.region_code.get() > 0:
            self.lastname.configure(state='disabled')
            self.firstname.configure(state='disabled')
            self.email.configure(state='disabled')
        else:
            self.lastname.configure(state='normal')
            self.firstname.configure(state='normal')
            self.email.configure(state='normal')

    def cancel_edit(self):
        """
        Cancels editing data (when 'Cancel' button is clicked).
        Hides the right pane, no changes are saved.
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
        self._clicked_del = False
        self._clicked_add = False
        self._clicked_upd = False


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


# import labels (en for English, ru for Russian)
with open(resource_path('labels_ru.pkl'), 'rb') as datafile:
    labels = pickle.load(datafile)

# import users
with open(resource_path('users.pkl'), 'rb') as datafile:
    users = pickle.load(datafile)

# import directors of departments
with open(resource_path('dept.pkl'), 'rb') as datafile:
    dept = pickle.load(datafile)

# import regions
with open(resource_path('regions.pkl'), 'rb') as datafile:
    regions = pickle.load(datafile)

# import texts
with open(resource_path('text.pkl'), 'rb') as datafile:
    text = pickle.load(datafile)

# start gui
root = tk.Tk()

# set styles
root.style = ttk.Style()
root.style.configure('.', font=('Arial', 13, 'normal'))
root.style.configure('TLabelFrame', borderwidth=3, relief='ridge', padding=5)
root.style.configure('Red.TLabel', foreground='red')
root.style.configure('Attachment.TLabel',
                     font=('Arial', 11, 'italic'), width=30)

# manage appearance
root.option_add("*TCombobox*Listbox*Font", ('Arial', 13))
root.title("GR Mailer v.1.01")
root.resizable(False, False)

# start app
app = Application(master=root)
main_window = MainWindow(master=app)
address_book = AddressBook(master=app)
app.add(main_window, text=labels['main'])
app.add(address_book, text=labels['address_book'])
app.mainloop()
