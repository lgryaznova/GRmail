"""
Settings class
"""
import tkinter as tk
import tkinter.ttk as ttk
from base_cls import StandardTab
from helper import labels, users

class Settings(StandardTab):
    """
    Third tab: settings
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(row=0, column=0)
        self.create_widgets()

    def create_widgets(self):
        """
        Create widgets
        """
        ############################################################
        # LEFT PANE
        ############################################################
        self.left_pane = ttk.LabelFrame(
            self, text=labels['general'], width=30)
        self.left_pane.grid(row=0, column=0, padx=10, pady=10, sticky='news')

        # use middlename
        self.use_middlename = tk.IntVar()
        self.use_middlename.set(1)
        self.middlename_cb = ttk.Checkbutton(
            self.left_pane, text=labels['use_middlename'],
            variable=self.use_middlename, onvalue=1, offvalue=0)
        self.middlename_cb.grid(row=0, column=0, pady=5, sticky='nw')

        # read receipt
        self.read_receipt = tk.IntVar()
        self.read_receipt.set(1)
        self.read_receipt_cb = ttk.Checkbutton(
            self.left_pane, text=labels['read_receipt'],
            variable=self.read_receipt, onvalue=1, offvalue=0)
        self.read_receipt_cb.grid(row=1, column=0, pady=5, sticky='nw')

        # set importance
        self.set_importance = tk.IntVar()
        self.set_importance.set(1)
        self.set_importance_cb = ttk.Checkbutton(
            self.left_pane, text=labels['set_importance'],
            variable=self.set_importance, onvalue=1, offvalue=0)
        self.set_importance_cb.grid(row=2, column=0, pady=5, sticky='nw')
        self.days_to_deadline = ttk.Entry(
            self.left_pane, font=('Arial', 13), width=3, justify=tk.RIGHT)
        self.days_to_deadline.insert(0, '5')
        self.days_to_deadline.grid(row=2, column=1, pady=5)
        self.days = ttk.Label(self.left_pane, text=labels['days'])
        self.days.grid(row=2, column=2, pady=5)

        # common buttons
        self.save_left = ttk.Button(
            self.left_pane, text=labels['save'], width=15)
        self.save_left.grid(row=3, column=0, columnspan=3, pady=20,
                            padx=50, sticky='wn')
        self.cancel_left = ttk.Button(
            self.left_pane, text=labels['cancel'], width=15)
        self.cancel_left.grid(row=3, column=0, columnspan=3, pady=20,
                              padx=50, sticky='en')
        self.default_left = ttk.Button(
            self.left_pane, text=labels['default'], width=20)
        self.default_left.grid(row=4, column=0, columnspan=3, pady=10,
                               sticky='n')

        ############################################################
        # RIGHT PANE
        ############################################################
        self.right_pane = ttk.LabelFrame(
            self, text=labels['network'], width=30)
        self.right_pane.grid(row=0, column=1, padx=10, pady=10, sticky='news')

        # profile
        self.profile = ttk.Label(self.right_pane, text=labels['profile'])
        self.profile.grid(row=0, column=0, pady=5, padx=2, sticky='en')
        self.username = ttk.Combobox(
            self.right_pane, values=users.keys(),
            state='readonly', font=('Arial', 13), width=25,
            postcommand=lambda: self.update_list(str(self.username),
                                                 users.keys()))
        self.username.grid(row=0, column=1, pady=5, sticky='news')

        # smtp server
        self.smtp_label = ttk.Label(self.right_pane, text=labels['smtp'])
        self.smtp_label.grid(row=1, column=0, pady=5, sticky='en')
        self.smtp_server = ttk.Entry(
            self.right_pane, font=('Arial', 13), width=35)
        self.smtp_server.grid(row=1, column=1, pady=5, sticky='news')

        # port
        self.port_label = ttk.Label(self.right_pane, text=labels['port'])
        self.port_label.grid(row=2, column=0, pady=5, padx=2, sticky='en')
        self.port = ttk.Entry(self.right_pane, font=('Arial', 13), width=5)
        self.port.grid(row=2, column=1, pady=5, sticky='nw')

        # use ssl
        self.use_ssl = tk.IntVar()
        self.use_ssl_cb = ttk.Checkbutton(
            self.right_pane, text=labels['use_ssl'],
            variable=self.use_ssl, onvalue=1, offvalue=0)
        self.use_ssl_cb.grid(row=3, column=1, pady=5, sticky='nw')

        # email
        self.email_label = ttk.Label(self.right_pane, text=labels['email'])
        self.email_label.grid(row=4, column=0, pady=5, padx=2, sticky='en')
        self.email = ttk.Entry(
            self.right_pane, font=('Arial', 13), width=30)
        self.email.grid(row=4, column=1, pady=5, sticky='news')

        # reply to corporate mail
        self.reply_to = tk.IntVar()
        self.reply_to.set(1)
        self.reply_to_cb = ttk.Checkbutton(
            self.right_pane, variable=self.reply_to,
            text=labels['reply_to_corp'], onvalue=1, offvalue=0)
        self.reply_to_cb.grid(row=5, column=1, columnspan=2,
                              pady=5, sticky='nw')

        # BCC to corporate email
        self.bcc_to_corp = tk.IntVar()
        self.bcc_to_corp.set(1)
        self.bcc_to_corp_cb = ttk.Checkbutton(
            self.right_pane, variable=self.bcc_to_corp,
            text=labels['bcc_to_corp'], onvalue=1, offvalue=0)
        self.bcc_to_corp_cb.grid(row=6, column=1, columnspan=2,
                                 pady=5, sticky='nw')

        # common buttons
        self.save_right = ttk.Button(
            self.right_pane, text=labels['save'], width=15)
        self.save_right.grid(row=7, column=0, columnspan=3, pady=20,
                             padx=50, sticky='wn')
        self.cancel_right = ttk.Button(
            self.right_pane, text=labels['cancel'], width=15)
        self.cancel_right.grid(row=7, column=0, columnspan=3, pady=20,
                               padx=50, sticky='en')
        self.default_right = ttk.Button(
            self.right_pane, text=labels['default'], width=20)
        self.default_right.grid(row=8, column=0, columnspan=3, pady=10,
                                sticky='n')


