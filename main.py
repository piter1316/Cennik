import tkinter as tk
import tkinter.ttk
from tkinter import messagebox, filedialog, ttk
from tkinter.ttk import Treeview
from typing import List, Any

import pymysql
import xlsxwriter

from Create_tool_tip import Create_tool_tip

# global variables
data: List[Any] = []
even = 0
how_many_added = 0


def connect_to_database(url, user, password, data_base_name):
    database_to_connect = pymysql.connect(url, user, password, data_base_name)
    global cursor
    cursor = database_to_connect.cursor()
    return database_to_connect


def disconnect_from_database(database_to_disconnect):
    database_to_disconnect.close()


def define_result_table(frame, mode, columns, style):
    table = tkinter.ttk.Treeview(frame, selectmode=mode, columns=columns, style=style)
    return table


def set_button_with_text(frame, text, command, row, column):
    button = tk.Button(frame, text=text, command=command)
    button.grid(row=row, column=column)
    return button


def set_button_with_img(frame, width, height, image, command, row, column, padx):
    button = tk.Button(frame, width=width, height=height, image=image, command=command)
    button.grid(row=row, column=column, padx=padx)
    return button


def set_label(frame, text, row, column):
    label = tk.Label(frame, text=text)
    label.grid(row=row, column=column)
    return label


def set_window(title, width, height, bg_color):
    window = tk.Tk()
    window.maxsize(width=width, height=height)
    window.minsize(width=width, height=height)
    window.title(title)
    window.configure(background=bg_color)
    ws = window.winfo_screenwidth()  # width of the screen
    hs = window.winfo_screenheight()
    x = (ws / 2) - (width / 2)
    y = (hs / 2) - (height / 2)
    window.geometry('100x100+{}+{}'.format(int(x), int(y)))
    return window


def set_input_field(frame, row, column, padx, relief):
    field = tk.Entry(frame, relief=relief)
    field.grid(row=row, column=column, padx=padx)
    return field


def set_result_table(tree_view_obj):
    tree_view_obj.heading("kodTowaru", text="kodTowaru")
    tree_view_obj.column("kodTowaru", width=130)

    tree_view_obj.heading("kontrahent", text="kontrahent")
    tree_view_obj.column("kontrahent", width=150)

    tree_view_obj.heading("cennik", text="cennik")
    tree_view_obj.column("cennik", width=80)

    tree_view_obj.heading("cenaKoncowa", text="cenaKoncowa[wal]")
    tree_view_obj.column("cenaKoncowa", width=110)

    tree_view_obj.heading("cenaKatalogowa", text="cenaKatalogowa[€]")
    tree_view_obj.column("cenaKatalogowa", width=110)

    tree_view_obj.heading("Rabat", text="Rabat")
    tree_view_obj.column("Rabat", width=50)

    tree_view_obj.heading("cenaKoncowaEUR", text="cenaKoncowa[€]")
    tree_view_obj.column("cenaKoncowaEUR", width=110)

    tree_view_obj.heading("zDnia", text="zDnia")
    tree_view_obj.column("zDnia", width=80)

    tree_view_obj['show'] = 'headings'

    return tree_view_obj


def show_table(tree_view_obj, row, column, ):
    tree_view_obj.grid(row=row, column=column)


def prepare_sql_select_query():
    kod_towaru = str(inputField_1.get())
    kod_towaru = kod_towaru.replace('"', '')
    kod_towaru = kod_towaru.replace("'", "")
    kod_towaru = kod_towaru.replace("&", "")
    kod_towaru = kod_towaru.replace("<!--", "")
    kod_towaru = kod_towaru.replace("-->", "")
    kod_towaru = kod_towaru.replace(">", "")
    kod_towaru = kod_towaru.replace("<", "")
    kod_towaru = kod_towaru.replace("$", "")
    kod_towaru = kod_towaru.replace("\r", "")
    kod_towaru = kod_towaru.replace("!", "")

    sql = "SELECT * FROM " \
          + \
          "`" + option_menu_value.get() + "`" \
          + " WHERE kodTowaru = '{}' ORDER BY cenaKoncowa_EUR".format(kod_towaru)
    return sql


def fetch_data_from_database():
    try:
        cursor.execute(prepare_sql_select_query())
        results = cursor.fetchall()
        return results
    except Exception:
        messagebox.showinfo("Błąd", "Podana Baza danych nie istnieje!")


def insert_data_into_table():
    global even
    global how_many_added

    how_many_added = 0
    if len(inputField_1.get()) == 0:
        messagebox.showinfo("Pusto", "PODAJ KOD!!!")
    elif len(fetch_data_from_database()) > 0:

        for row in fetch_data_from_database():

            kod_towaru = row[0]
            kontrahent = row[1]
            kontrahent_cennik = row[2]
            cena_koncowa = row[7]
            cena_katalogowa_eur = row[8]
            rabat = row[10]
            z_dnia = row[11]
            cena_kon_eur = row[9]

            if cena_katalogowa_eur is not None:
                cena_katalogowa_eur = round(cena_katalogowa_eur, 2)
            else:
                cena_katalogowa_eur = ""

            if cena_kon_eur is not None:
                cena_kon_eur = round(cena_kon_eur, 2)
            else:
                cena_kon_eur = ""

            if rabat is not None:
                rabat = round(rabat, 2)
            else:
                rabat = ""

            product = [kod_towaru, kontrahent, kontrahent_cennik, cena_koncowa, cena_katalogowa_eur, rabat,
                       cena_kon_eur, z_dnia]
            data.append(product)

            how_many_added += 1

            if even % 2 == 0:
                result_table.insert("", "end", values=(
                    kod_towaru, kontrahent, kontrahent_cennik, cena_koncowa, cena_katalogowa_eur, rabat,
                    cena_kon_eur,
                    z_dnia), tags='evenrow')

            else:
                result_table.insert("", "end", values=(
                    kod_towaru, kontrahent, kontrahent_cennik, cena_koncowa, cena_katalogowa_eur, rabat,
                    cena_kon_eur,
                    z_dnia), tags='oddrow')
        even += 1
        inputField_1.delete(0, 'end')
    else:

        messagebox.showerror("NIE ZNALEZIONO", "BRAK KODU W BAZIE")



def click_search_button():
    fetch_data_from_database()
    insert_data_into_table()
    button_active(data)


def click_export():
    export_to_xls(data)


def click_clear_results():
    for node in result_table.get_children():
        result_table.delete(node)
    for i in range(len(data)):
        data.pop()
    inputField_1.delete(0, 'end')
    button_active(data)


def click_undo_button():
    undo_search()
    undo_button.config(state=tk.DISABLED)
    inputField_1.delete(0, 'end')


def export_to_xls(data_as_list):
    save_directory = filedialog.asksaveasfilename(initialdir="/",
                                                  title="Select file",
                                                  filetypes=(("Excel", "*.xlsx"), ("all files", "*.*")),
                                                  defaultextension='.xlsx')
    try:
        workbook = xlsxwriter.Workbook(save_directory)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0,
                            ["kodTowaru", "kontrahent", "cennik", "cenaKoncowa_WAL", "cenaKatalogowa_EUR", "Rabat",
                             "cenaKoncowa_EUR", "zDnia"])
        row = 0

        for col, data_as_list in enumerate(data_as_list):
            col += 1
            worksheet.write_row(col, row, data_as_list)
        workbook.close()
        messagebox.showinfo('ZAPISANO', "ZAPISANO w Lokalizacji: {}".format(save_directory))
    except Exception:
        messagebox.showinfo("ANULOWANO", "ANULOWANO ZAPIS")


def get_tables_list():
    cursor.execute("SHOW TABLES in b2b_robocza LIKE 'zestaw%Cennik' ")
    tables = cursor.fetchall()
    list_items: List[Any] = []

    for (table_name,) in tables:
        list_items.append(table_name)
    return list_items


def undo_search():
    global how_many_added
    global even

    if len(data) > 0:

        for i in range(len(data) - how_many_added, len(data)):
            data.pop()

        all_nodes = []
        for element in result_table.get_children():
            all_nodes.append(element)

        nodes_to_delete = []
        for i in range(len(all_nodes) - how_many_added, len(all_nodes)):
            nodes_to_delete.append(all_nodes[i])

        for node in nodes_to_delete:
            result_table.delete(node)
    else:
        pass
    how_many_added = 0
    even += 1
    button_active(data)


def button_active(list_with_data):
    if len(list_with_data) == 0:
        export_button.config(state=tk.DISABLED)
        undo_button.config(state=tk.DISABLED)
        clear_button.config(state=tk.DISABLED)
    else:
        export_button.config(state=tk.NORMAL)
        undo_button.config(state=tk.NORMAL)
        clear_button.config(state=tk.NORMAL)


def press_enter_to_search(event):
    click_search_button()


# main

window_1 = set_window('CENNIK', 900, 450, '#c6c3c0')


window_1.bind('<Return>', press_enter_to_search)

icon = tk.PhotoImage(file='img/indeks.png')
window_1.tk.call('wm', 'iconphoto', window_1._w, icon)

tool_bar = tk.Frame(window_1)
tool_bar.pack(side=tk.TOP, fill=tk.Y)
tool_bar.configure(background='#c6c3c0')

result_field = tk.Frame(window_1)
result_field.pack(side=tk.TOP, fill=tk.Y)
result_field.configure(background='#c6c3c0')

database = connect_to_database('b2b.int-technics.pl', 'b2b_roboczy', 'b2b_roboczy', 'b2b_robocza')

result_table: Treeview = define_result_table(result_field, "extended", (
    "kodTowaru", "kontrahent", "cennik", "cenaKoncowa", "cenaKatalogowa", "Rabat", "cenaKoncowaEUR", "zDnia"),
                                   "Custom.Treeview")

scrollbar = tk.Scrollbar(result_field, orient="vertical", command=result_table.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_table.configure(yscrollcommand=scrollbar.set)
search_text_label = set_label(tool_bar, 'Podaj kod Towaru: ', 0, 1)
search_text_label.configure(background='#c6c3c0')

inputField_1 = set_input_field(tool_bar, 0, 2, 5, tk.RAISED)
inputField_1.focus()

search_img = tk.PhotoImage(file='img/search.png')
search_button = set_button_with_img(tool_bar, 20, 20, search_img, click_search_button, 0, 4, 1)
search_button_tip = Create_tool_tip(search_button, "WYSZUKAJ", '#FF6B00')

clear_button_img = tk.PhotoImage(file='img/clear_all.png')
clear_button = set_button_with_img(tool_bar, 20, 20, clear_button_img, click_clear_results, 0, 5, 1)
clear_button.config(state=tk.DISABLED)
clear_button_tip = Create_tool_tip(clear_button, 'Wyczyść wyszukiwania', 'black', 'white')

export_img = tk.PhotoImage(file='img/Excel-icon.png')
export_button = set_button_with_img(tool_bar, 20, 20, export_img, click_export, 0, 6, 1)
export_button.config(state=tk.DISABLED)
export_button_tip = Create_tool_tip(export_button, "Export do EXCELA", '#1D7044', 'white')

undo_img = tk.PhotoImage(file='img/undo.gif')
undo_button = set_button_with_img(tool_bar, 20, 20, undo_img, click_undo_button, 0, 7, 1)
undo_button.config(state=tk.DISABLED)
undo_button_tip = Create_tool_tip(undo_button, "Cofnij wyszukiwanie", '#396ED6', 'white')

option_menu_value = tk.StringVar(window_1)
option_menu_value.set(get_tables_list()[0])

tables_list = tk.OptionMenu(tool_bar, option_menu_value, *get_tables_list())
tables_list.grid(row=0, column=3, padx=5)
tables_list_tip = Create_tool_tip(tables_list, 'Wybierz cennik', 'yellow')

# table with query results
set_result_table(result_table)
result_table.pack(side=tk.LEFT, fill=tk.X)

# style of table
result_table_style = ttk.Style(result_field)
result_table_style.theme_use("clam")
result_table_style.configure("Treeview", background="#FFE4C4",
                             fieldbackground="#FFE4C4", foreground="black")

# table colors for different search
result_table.tag_configure('oddrow', background='orange')
result_table.tag_configure('evenrow', background='OrangeRed')

window_1.mainloop()
disconnect_from_database(database)
