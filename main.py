import tkinter as tk
import tkinter.ttk
from tkinter import messagebox, filedialog, ttk
from typing import List, Any
import pymysql
import xlsxwriter

data = []
even = 0


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


def set_result_table(result_table):
    result_table.heading("kodTowaru", text="kodTowaru")
    result_table.column("kodTowaru", width=130)

    result_table.heading("kontrahent", text="kontrahent")
    result_table.column("kontrahent", width=150)

    result_table.heading("cennik", text="cennik")
    result_table.column("cennik", width=80)

    result_table.heading("cenaKoncowa", text="cenaKoncowa[wal]")
    result_table.column("cenaKoncowa", width=110)

    result_table.heading("cenaKatalogowa", text="cenaKatalogowa[€]")
    result_table.column("cenaKatalogowa", width=110)

    result_table.heading("Rabat", text="Rabat")
    result_table.column("Rabat", width=50)

    result_table.heading("cenaKoncowaEUR", text="cenaKoncowa[€]")
    result_table.column("cenaKoncowaEUR", width=110)

    result_table.heading("zDnia", text="zDnia")
    result_table.column("zDnia", width=80)

    result_table['show'] = 'headings'

    return result_table


def show_table(result_table, row, column, ):
    result_table.grid(row=row, column=column)


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
    if len(fetch_data_from_database()) > 0:


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

            cena_kon_eur = round(cena_kon_eur, 2)
            rabat = round(rabat, 2)

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

        #messagebox.showinfo("Błąd POBIERANIA DANYCH")

    else:
        messagebox.showinfo("NIE ZNALEZIONO", "BRAK KODU W BAZIE")


def click_search_button():
    global even
    even += 1
    fetch_data_from_database()
    insert_data_into_table()


def export_to_xls(data):
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

        for col, data in enumerate(data):
            col = col + 1
            worksheet.write_row(col, row, data)
        workbook.close()
        messagebox.showinfo('ZAPISANO', "ZAPISANO w Lokalizacji: {}".format(save_directory))
    except:
        messagebox.showinfo("ANULOWANO", "ANULOWANO ZAPIS")


def click_export():
    export_to_xls(data)


def get_tables_list():
    cursor = database.cursor()
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
    for i in result_table.get_children():
        result_table.delete(i)
    for i in range(len(data)):
        data.pop()


# main
window_1 = set_window('CENNIK', 1000, 480)

database = connect_to_database('b2b.int-technics.pl', 'b2b_roboczy', 'b2b_roboczy', 'b2b_robocza')

result_table = define_result_table(window_1, "extended", (
    "kodTowaru", "kontrahent", "cennik", "cenaKoncowa", "cenaKatalogowa", "Rabat", "cenaKoncowaEUR", "zDnia"),
                                   "Custom.Treeview")

set_result_table(result_table)
show_table(result_table, 0, 0)
style = ttk.Style(window_1)
style.theme_use("clam")
style.configure("Treeview", background="#FFE4C4",
                fieldbackground="#FFE4C4", foreground="black")

result_table.tag_configure('oddrow', background='orange')
result_table.tag_configure('evenrow', background='OrangeRed')

searchButton = set_button(window_1, 'WYSZUKAJ', click_search_button, 5, 0)

clearButton = set_button(window_1, "WYCZYŚć WYSZUKIWANIE", click_clear_results, 6, 0)

exportButton = set_button(window_1, "Export do pliku .xlsx", click_export, 8, 0)

searchTextLabel = set_label(window_1, 'Podaj kod Towaru: ', 1, 0)

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
