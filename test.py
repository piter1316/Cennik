from tkinter import *

from tkinter import ttk

root = Tk()

root.minsize(width=1460, height=800)

root.maxsize(width=1460, height=800)

entry = Entry(root)

entry.pack()

frame = Frame(root, height=800, width=760, bg="white")

tree = ttk.Treeview(frame, height="800")

columns = tree.column("#0", minwidth=5000, width="500", stretch=True)

tree.insert("" , 0,    text="Line 1")

id2 = tree.insert("", 1, "dir2", text="Dir 2")

tree.insert(id2, "end", "dir 2", text="sub dir 2")

id3 = tree.insert("", 2, "dir3", text="Dir 3")

tree.insert(id3, "end", "dir 3", text="sub dir 3")

id4 = tree.insert("", 3, "dir4", text="Dir 4")

tree.insert(id4, "end", "dir 4", text="sub dir 4")

id5 = tree.insert("", 4, "dir5", text="Dir   5..............................")

tree.insert(id4, "end", "dir 5", text="sub dir 5")

id6 = tree.insert("", 5, "dir6", text="Dir 6")

tree.insert(id6, "end", "dir 6", text="sub dir 6vvvvvvvvvvvvvvvvv5vvvvvvv")



def copy(a):

    curItem = tree.focus()

    item_dict = tree.item(curItem)

    #print (item_dict['text'])
    return item_dict['text']

def paste(event):
    text = tree.selection_get(selection='CLIPBOARD')
    print(text)
    return text


tree.bind('<Control-c>', copy)
tree.bind('<Control-v>', paste)


scrollbar = Scrollbar(frame)

tree.config(yscrollcommand=scrollbar.set)



scrollbar.config(command = tree.yview )



scrollbar1 = Scrollbar(frame, orient = HORIZONTAL)

tree.config(xscrollcommand=scrollbar1.set)

scrollbar1.config(command = tree.xview )

scrollbar.pack(side = RIGHT, fill=Y)

scrollbar1.pack(side = BOTTOM, fill=X)

tree.pack(side=LEFT)

frame.pack(side=LEFT)

root.mainloop() 
