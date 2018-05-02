import tkinter as tk
import tkinter.ttk
from tkinter import messagebox, filedialog, ttk
from typing import List, Any

import pymysql
import xlsxwriter

# global variables
data = []
even = 0
how_many_added = 0


def connect_to_database(url, user, password, data_base_name):
    database = pymysql.connect(url, user, password, data_base_name)
    global cursor
    cursor = database.cursor()
    return database


def disconect_from_database(database):
    database.close()


def define_result_table(frame, mode, columns, style):
    table = tkinter.ttk.Treeview(frame, selectmode=mode, columns=columns, style=style)
    return table


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
          "`" + optionMenuValue.get() + "`" \
          + " WHERE kodTowaru = '{}' ORDER BY cenaKoncowa_EUR".format(kod_towaru)
    return sql


def fetch_data_from_database():
    try:
        cursor.execute(prepare_sql_select_query())
        results = cursor.fetchall()
    except:
        messagebox.showinfo("Błąd", "Podana Baza danych nie istnieje!")

    return results


def insert_data_into_table():
    global how_many_added
    how_many_added = 0
    if len(inputField_1.get()) == 0:
        messagebox.showinfo("Pusto","PODAJ KOD!!!")
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

            product = []
            product.append(kod_towaru)
            product.append(kontrahent)
            product.append(kontrahent_cennik)
            product.append(cena_koncowa)
            product.append(cena_katalogowa_eur)
            product.append(rabat)
            product.append(cena_kon_eur)
            product.append(z_dnia)
            data.append(product)

            how_many_added += 1
            # undo_button.config(state=tk.NORMAL)
            # clear_button.config(state=tk.NORMAL)
            button_active(data)

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

    else:
        messagebox.showinfo("NIE ZNALEZIONO", "BRAK KODU W BAZIE")


def click_search_button():
    global even
    even += 1
    fetch_data_from_database()
    insert_data_into_table()


def export_to_xls(data_as_list):
    save_directory = filedialog.asksaveasfilename(initialdir="/",
                                                  title="Select file",
                                                  filetypes=(("Excel", "*.xlsx"), ("all files", "*.*")),
                                                  defaultextension='.xlsx')
    try:
        workbook = xlsxwriter.Workbook(save_directory)
        worksheet = workbook.add_worksheet()
        worksheet.write_row(0, 0, ["kodTowaru", "kontrahent", "cennik", "cenaKoncowa", "cenaKatalogowa_EUR", "Rabat",
                                   "cenaKoncowaEUR", "zDnia"])
        row = 0

        for col, data_as_list in enumerate(data_as_list):
            col += 1
            worksheet.write_row(col, row, data_as_list)
        workbook.close()
        messagebox.showinfo('ZAPISANO', "ZAPISANO w Lokalizacji: {}".format(save_directory))
    except:
        messagebox.showinfo("ANULOWANO", "ANULOWANO ZAPIS")


def click_export():
    export_to_xls(data)


def get_tables_list():
    #cursor = database.cursor()
    cursor.execute("SHOW TABLES in b2b_robocza LIKE 'zestaw%Cennik' ")
    tables = cursor.fetchall()
    list_items: List[Any] = []

    for (table_name,) in tables:
        list_items.append(table_name)
    return list_items


def set_button(frame, text, command, row, column):
    button = tk.Button(frame, text=text, command=command)
    button.grid(row=row, column=column)
    return button


def set_label(frame, text, row, column):
    label = tk.Label(frame, text=text)
    label.grid(row=row, column=column)
    return label


def set_window(title, width, height):
    window = tk.Tk()
    window.maxsize(width=width, height=height)
    window.minsize(width=width, height=height)
    window.title(title)
    return window


def set_input_field(frame, row, column):
    field = tk.Entry(frame)
    field.grid(row=row, column=column)
    return field


def click_clear_results():
    for node in result_table.get_children():
        result_table.delete(node)
    for i in range(len(data)):
        data.pop()
    clear_button.config(state=tk.DISABLED)
    undo_button.config(state=tk.DISABLED)
    button_active(data)


def undo_search():
    global how_many_added
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
    global even
    even += 1
    undo_button.config(state=tk.DISABLED)

    button_active(data)


def click_undo_button():
    undo_search()
    undo_button.config(state=tk.DISABLED)

def button_active(list):
    if len(list) == 0:
        export_button.config(state=tk.DISABLED)
        undo_button.config(state=tk.DISABLED)
        clear_button.config(state=tk.DISABLED)
    else:
        export_button.config(state=tk.NORMAL)
        undo_button.config(state=tk.NORMAL)
        clear_button.config(state=tk.NORMAL)

window_1 = set_window('CENNIK', 1000, 480)

database = connect_to_database('b2b.int-technics.pl', 'b2b_roboczy', 'b2b_roboczy', 'b2b_robocza')

result_table = define_result_table(window_1, "extended", (
    "kodTowaru", "kontrahent", "cennik", "cenaKoncowa", "cenaKatalogowa", "Rabat", "cenaKoncowaEUR", "zDnia"),
                                   "Custom.Treeview")

#table with query results
set_result_table(result_table)
show_table(result_table, 0, 0)

# style of table
style = ttk.Style(window_1)
style.theme_use("clam")
style.configure("Treeview", background="#FFE4C4",
                fieldbackground="#FFE4C4", foreground="black")

#table colors for different search
result_table.tag_configure('oddrow', background='orange')
result_table.tag_configure('evenrow', background='OrangeRed')

search_button = set_button(window_1, 'WYSZUKAJ', click_search_button, 5, 0)

clear_button = set_button(window_1, "WYCZYŚć WYSZUKIWANIE", click_clear_results, 6, 0)
clear_button.config(state=tk.DISABLED)

export_button = set_button(window_1, "Export do pliku .xlsx", click_export, 8, 0)
export_button.config(state=tk.DISABLED)

undo_button = set_button(window_1, "Cofinj wyszukiwanie", click_undo_button, 9, 0)
if len(data)>0:
    undo_button.config(state=tk.NORMAL)
else:
    undo_button.config(state=tk.DISABLED)

search_text_label = set_label(window_1, 'Podaj kod Towaru: ', 1, 0)

inputField_1 = set_input_field(window_1, 2, 0)
inputField_1.focus()

scrollbar = tk.Scrollbar(window_1, command=result_table.yview)
scrollbar.grid(row=0, column=2, sticky=tk.N)

optionMenuValue = tk.StringVar(window_1)
optionMenuValue.set(get_tables_list()[0])

tables_list = tk.OptionMenu(window_1, optionMenuValue, *get_tables_list())
tables_list.grid(row=3, column=0, rowspan=2, sticky=tk.N)

window_1.mainloop()
disconect_from_database(database)
