import tkinter as tk

def set_button_with_text(frame, text, command, row, column):
    button = tk.Button(frame, text=text, command=command)
    button.grid(row=row, column=column)
    return button


def set_button_with_img(frame, width, height, image, command, row, column, padx=0):
    button = tk.Button(frame, width=width, height=height, image=image, command=command)
    button.grid(row=row, column=column, padx=padx)
    return button