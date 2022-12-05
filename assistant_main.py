import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from modules import bs_tests

name = ""

window = tk.Tk()
t = Toplevel(window)
content = ttk.Frame(window)
frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
side_bar = ttk.Frame(content, borderwidth=5, relief="ridge", width=75, height=100)
comm_tab = ttk.Button(side_bar, text="set comm")

content.grid(column=0, row=0)
side_bar.grid(column=0, row=0, columnspan=1, rowspan=2)
comm_tab.grid(column=0, row=0)
frame.grid(column=1, row=0, columnspan=3, rowspan=2)
window.mainloop()