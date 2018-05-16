import tkinter as tk

def set_window(title, width, height, bg_color):
    window = tk.Toplevel()
    window.maxsize(width=width, height=height)
    window.minsize(width=width, height=height)
    window.title(title)
    window.configure(background=bg_color)
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()
    x = (ws / 2) - (width / 2)
    y = (hs / 2) - (height / 2)
    window.geometry('{}x{}+{}+{}'.format(int(width), int(height), int(x), int(y)))
    return window