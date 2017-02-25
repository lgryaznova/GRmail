"""
Tkinter root window
"""
import tkinter as tk
import tkinter.ttk as ttk

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
root.title("GR Mailer v.1.03")
root.resizable(False, False)
