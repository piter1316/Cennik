import tkinter as tk


class RightClickMenu(tk.Frame):
   def __init__(self, parent, text_area):
       self.master = parent
       tk.Frame.__init__(self, self.master)
       self.text_area = text_area
       self.create_widgets()

   def create_widgets(self):
       self.create_right_click_menu()

   def create_right_click_menu(self):
       self.right_click_menu = tk.Menu(self.master, tearoff=0, relief='sunken')
       self.right_click_menu.add_command(label="Copy", command=self.copy_text)
       self.right_click_menu.add_separator()
       self.right_click_menu.add_command(label="Paste", command=self.paste_text)
       self.right_click_menu.add_separator()
       self.right_click_menu.add_command(label="Clear", command=self.clear_text)

   def popup_text(self, event):
       self.right_click_menu.post(event.x_root, event.y_root)

   def copy_text(self):
       if self.text_area.tag_ranges("sel"):
           text = self.text_area.get("sel.first", "sel.last")
           self.clipboard_append(text)

   def paste_text(self):
       self.text_area.insert(tk.INSERT, self.clipboard_get())

   def clear_text(self):
       self.text_area.delete(1.0, tk.END)