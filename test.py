from tkinter import *

def click():
    print(entry.get())
okno = Tk()

entry = Entry()
entry.pack()
b = Button(okno, text="OK", command=click)
b.pack()
okno.mainloop()