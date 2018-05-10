import tkinter  as tk
import tkinter.ttk

root = tk.Tk()

tree = tkinter.ttk.Treeview(root)

tree["columns"] = ("one", "two")
tree.column("one", width=100)
tree.column("two", width=100)
tree.heading("one", text="coulmn A")
tree.heading("two", text="column B")

tree.insert("", 0, text="KodTowaru")

tree.insert("", 1, "dir2", text="1234654")
tree.insert("dir2", "end", "dir 2", text="", values=("2A", "2B"))
#tree.insert("dir2", "end", "dir 2", text="", values=("2", "2"))
tree.pack()
root.mainloop()