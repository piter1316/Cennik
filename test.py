from tkinter import ttk
import tkinter as tk
from popup import RightClickMenu


class MyTestApp(tk.Frame):
   def __init__(self, parent):
       self.master = parent
       tk.Frame.__init__(self, self.master)
       self.configure_gui()
       self.create_widgets()
       self.bind_right_click_menu_to_typing_area()

   def configure_gui(self):
       self.master.title('MY Test App')

   def create_widgets(self):
       self.create_text_area()
       self.create_exit_button()

   def create_text_area(self):
       self.text_area = tk.Text(self.master, borderwidth=2, relief='sunken')
       self.text_area.config(height=30, width=80)
       self.text_area.grid(row=0, column=0, sticky="new")

   def create_exit_button(self):
       self.exit_btn = ttk.Button(self.master, text='Exit', command=self.exit_application)
       self.exit_btn.grid(row=1, column=0, sticky='W', pady=15)

   def bind_right_click_menu_to_typing_area(self):
       self.popup = RightClickMenu(self.master, self.text_area)
       self.text_area.bind("<Button-3>", self.popup.popup_text)

   def exit_application(self):
       self.master.destroy()

def main():
   root = tk.Tk()
   MyTestApp(root)
   root.mainloop()

if __name__ == '__main__':
   main()