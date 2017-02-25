"""
MainWindow class
"""
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fdialog
import win32com.client
import re
import os
from datetime import datetime, timedelta, date
from base_cls import StandardTab
from autocomplete import AutocompleteCombobox
from root import root
from helper import labels, users, dept, regions, text, process_region

class MainWindow(StandardTab):
    """
    First tab: main window of the app
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0)
        self._current_msg = None
        self._last_msg =[]
        self.create_widgets()

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
            self.left_pane, values=users.keys(), state='readonly',
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
        self.region.set_completion_list(regions.keys())
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
        self.attach = ''
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
            style='Generate.TButton', command=self.generate_letter)
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
            self.right_pane, text=labels['send'], command=self.send_mail)
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
        dialog and proceed accordingly (see self.show_attachment).
        'Off' state means no attachment, so we reset the variable
        holding paths to attachments (self.attach) to default and
        display standard text instead of filenames of attachments.
        """
        if not self.attach_flag.get():
            self.attach = ''
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
            elif regions[self.region.get()].regtype > 0:
                # update error field
                if regions[self.region.get()].regtype == 1:
                    self.errors['text'] = (process_region(self.region.get())
                                           + labels['error_region1'])
                elif regions[self.region.get()].regtype == 2:
                    self.errors['text'] = (process_region(self.region.get())
                                           + labels['error_region2'])
                elif regions[self.region.get()].regtype == 3:
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
        # check attachments
        if not isinstance(self.attach, tuple):
            self.errors['text'] += labels['error_no_attachment']
            self.attach_name.configure(style='Red.TLabel')
            attach_flag = False
        # check reasonning
        if self.reason.get('1.0', 'end').strip() == '':
            self.reason_label.configure(style='Red.TLabel')
            flag = False

        # update error message field
        if not flag:
            self.errors['text'] += labels['error_empty_field']

        # if check is passed, generate a letter
        return flag and attach_flag

    def generate_letter(self):
        """
        Returns a new letter instead of the old one (string)
        """
        # proceed only if input is OK
        if not self.check_input():
            return

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

        # assign user input values to local variables
        region = process_region(self.region.get())
        customer = self.customer.get().strip()
        reasoning = self.reason.get('1.0', 'end-1c').strip()
        signature = users[self.username.get()].signature

        # assign director name and update headers: TO
        if self.legal_fwd.get():
            self.addr_to.insert(0, dept['Legal'].email)
            director = dept.appeal('Legal', flag=True)
        else:
            self.addr_to.insert(0, regions[self.region.get()].email)
            director = regions.appeal(self.region.get(), flag=True)

        # update headers: CC
        cc_list = []
        if self.gr_cc.get():
            cc_list.append(dept['GR'].email)
        if self.legal_cc.get():
            cc_list.append(dept['Legal'].email)
        self.addr_cc.insert(0, ';'.join(cc_list))

        # update headers: SUBJ
        if self.region.get() == '':
            subject = text['subjText'].format(customer, reasoning)
        else:
            subject = text['subjTextRegion'].format(customer, region, reasoning)

        # append due date if any
        deadline = self.process_date(self.deadline.get())
        if deadline is not None:
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

    def send_mail(self):
        """
        Sends the generated email after field validation. Displays
        the corresponding message. Prevents multiple sending.

        First, tries to send via Outlook. If no success, tries
        specified email settings. Otherwise, copies subject and
        body of the email to the clipboard.
        """
        # proceed only if input is OK
        if not self.check_input():
            return

        # reset error messages
        self.errors['text'] = ''

        # store current message to prevent double sending
        self._current_msg = hash(self.addr_to.get() + self.addr_cc.get()
                                 + self.subj.get('1.0', 'end-1c')
                                 + ''.join(self.attach)
                                 + self.body.get('1.0', 'end-1c'))

        # do not allow to send duplicate message
        if self._current_msg in self._last_msg:
            self.errors['text'] = labels['duplicate_email']
            return

        # try to send through Outlook
        try:
            start_item = 0x0
            obj = win32com.client.Dispatch('Outlook.Application')
            new_mail = obj.CreateItem(start_item)
            new_mail.Subject = self.subj.get('1.0', 'end-1c')
            new_mail.Body = self.body.get('1.0', 'end-1c')
            new_mail.To = ';'.join(re.split('[\s;,]+', self.addr_to.get()))
            new_mail.CC = ';'.join(re.split('[\s;,]+', self.addr_cc.get()))
            for i in self.attach:
                new_mail.Attachments.Add(os.path.normpath(i))
            new_mail.Send()
            self.errors['text'] = labels['message_sent']
        except Exception:
            # try network settings, if not - show error
            try:
                self.errors['text'] = labels['outlook_error']
                raise Exception
            except Exception:
                # copy email to the clipboard
                self.errors['text'] = labels['copy_clipboard']
                root.clipboard_clear()
                root.clipboard_append(self.subj.get('1.0', 'end-1c') + '\n\n'
                                      + self.body.get('1.0', 'end-1c'))
        finally:
            # store only last 20 emails of the current session
            if len(self._last_msg) >= 20:
                del self._last_msg[0]
            self._last_msg.append(self._current_msg)
