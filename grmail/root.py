"""
Tkinter root window
"""
import tkinter as tk
import tkinter.ttk as ttk
from helper import FONT_M, FONT_ITAL

# start gui
root = tk.Tk()

# set styles
root.style = ttk.Style()
root.style.configure('.', font=FONT_M)
root.style.configure('TLabelFrame', borderwidth=3, relief='ridge', padding=5)
root.style.configure('Red.TLabel', foreground='red')
root.style.configure('Attachment.TLabel',
                     font=FONT_ITAL, width=30)

# manage appearance
root.option_add("*TCombobox*Listbox*Font", FONT_M)
root.title("GR Mailer v.1.03")
root.resizable(False, False)
