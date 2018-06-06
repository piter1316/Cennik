import os
import sys
import tkinter as tk
import tkinter.ttk
from tkinter import messagebox, filedialog, ttk, Label
from tkinter.ttk import Treeview
from typing import List, Any

import pymysql
import xlsxwriter

import button
import top_window
import window
from Create_tool_tip import Create_tool_tip

# global variables
even = 0
data: List[Any] = []
how_many_added = 0
just_opened = 0


def connect_to_database(url, user, password, data_base_name):
    try:
        database_to_connect = pymysql.connect(url, user, password, data_base_name)
        global cursor
        cursor = database_to_connect.cursor()
        return database_to_connect
    except pymysql.err.OperationalError:
        messagebox.showerror("Błąd", "NIE Połączono w bazą danych")


def disconnect_from_database(database_to_disconnect):
    database_to_disconnect.close()


def define_result_table(frame, mode, columns, style, height):
    table = tkinter.ttk.Treeview(frame, selectmode=mode, columns=columns, style=style, height=height)
    return table


def set_label(frame, text, row, column, bg):
    label: Label = tk.Label(frame, text=text, bg=bg)
    label.grid(row=row, column=column)
    return label


def set_input_field(frame, row, column, padx, relief, width):
    field = tk.Entry(frame, relief=relief)
    field.grid(row=row, column=column, padx=padx)
    field.config(width=width)
    return field


def set_multiple_input_field(frame, row, column, padx, relief, width, height):
    multiple_field = tk.Text(frame, relief=relief, width=width, height=height)
    multiple_field.grid(row=row, column=column, padx=padx)
    return multiple_field


def set_result_table(tree_view_obj):
    tree_view_obj.heading("kodTowaru", text="kodTowaru")
    tree_view_obj.column("kodTowaru", width=130, anchor='center')

    tree_view_obj.heading("kontrahent", text="kontrahent")
    tree_view_obj.column("kontrahent", width=150, anchor='center')

    tree_view_obj.heading("cennik", text="cennik")
    tree_view_obj.column("cennik", width=90, anchor='center')

    tree_view_obj.heading("cenaKoncowa", text="cenaKoncowa[wal]")
    tree_view_obj.column("cenaKoncowa", width=110, anchor='center')

    tree_view_obj.heading("cenaKatalogowa", text="cenaKatalogowa[€]")
    tree_view_obj.column("cenaKatalogowa", width=110, anchor='center')

    tree_view_obj.heading("Rabat", text="Rabat")
    tree_view_obj.column("Rabat", width=50, anchor='center')

    tree_view_obj.heading("cenaKoncowaEUR", text="cenaKoncowa[€]")
    tree_view_obj.column("cenaKoncowaEUR", width=110, anchor='center')

    tree_view_obj.heading("zDnia", text="zDnia")
    tree_view_obj.column("zDnia", width=80, anchor='center')

    tree_view_obj['show'] = 'headings'
    return tree_view_obj


def show_table(tree_view_obj, row, column, ):
    tree_view_obj.grid(row=row, column=column)


def secure_sql_query(args):
    kod_towaru = str(args)
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
    return kod_towaru


def insert_search_into_table(limit):
    whole_text_from_multiple_input_field = multiple_input_field.get("1.0", tk.END)
    multiple_codes_to_search = []
    for item in whole_text_from_multiple_input_field.splitlines():
        item = item.replace(" ", "")
        item = secure_sql_query(item)
        if item != '':
            multiple_codes_to_search.append(item)
    added = 0

    for code in multiple_codes_to_search:
        cursor.execute("SELECT * FROM "
                       + "`" + option_menu_value.get() + "`"
                       + " WHERE kodTowaru = '{}' ORDER BY cenaKoncowa_EUR {}".format(code, limit))
        result = cursor.fetchall()

        if len(result) > 0:
            for row in result:

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
                added += 1

                values = tuple(product)

                if added % 2 == 0:

                    result_table.insert("", "end", values=values, tags='evenrow')
                else:
                    result_table.insert("", "end", values=values, tags='oddrow')
        else:
            data.append([code, '-----', '-----', 'BRAK TOWARU', '-----', '-----', 0, '-----'])
            result_table.insert("", "end", values=(code, '-----', '-----', 'BRAK TOWARU', '-----', '-----', 0, '-----'),
                                tags='empty')


def show_only_lowest_prices():
    insert_search_into_table("LIMIT 1")
    button_active(data)
    calculate_sum()


def search():
    insert_search_into_table("")
    button_active(data)


def click_search_button():
    search()
    # calculate_sum()


def click_export():
    export_to_xls(data)


def clear_results():
    for node in result_table.get_children():
        result_table.delete(node)
    for i in range(len(data)):
        data.pop()
    sum_field.config(text='            ')
    button_active(data)


def click_clear_results():
    clear_results()


def click_undo_button():
    undo_search()


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

    except IOError:
        messagebox.showinfo("ANULOWANO", "ANULOWANO ZAPIS")


def get_tables_list():
    cursor.execute("SHOW TABLES in b2b_robocza LIKE 'zestaw%Cennik' ")
    tables = cursor.fetchall()
    list_items: List[Any] = []

    for (table_name,) in tables:
        list_items.append(table_name)
    return list_items


def get_tables_list_to_add_data():
    cursor.execute("SHOW TABLES in b2b_robocza LIKE '\__%Cennik' ")
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
    # calculate_sum()
    button_active(data)


def button_active(list_with_data):
    if len(list_with_data) == 0:
        export_button.config(state=tk.DISABLED)
        clear_button.config(state=tk.DISABLED)
    else:
        export_button.config(state=tk.NORMAL)
        clear_button.config(state=tk.NORMAL)


def press_enter_to_perform_multiple_search(event):
    click_search_button()
    return event


def calculate_sum():
    prices = []
    for i in range(len(data)):
        prices.append(data[i][6])

    sum_field.config(text=str(sum(prices)))


def clear_multiple_input_field():
    multiple_input_field.delete("1.0", tk.END)


def open_add_window():
    add_window.deiconify()
    kod_towaru_input_field.focus_set()


def close_add_window():
    add_window.withdraw()


def add_data_to_database():
    if database is None:
        messagebox.showinfo("!!!", "BRAK POŁĄCZENIA")
        open_add_window()
    else:
        kod_towaru = kod_towaru_input_field.get()
        kod_towaru = secure_sql_query(kod_towaru)
        kod_towaru = kod_towaru.replace("\n","")
        kontrahent_kod = kontrahent_input_field.get()
        kontrahent_cennik = kontrahent_cenni_input_field.get()
        opis = opis_input_field.get()
        cena_katalogowa = cena_katalogowa_input_field.get()
        waluta = waluta_input_field.get()
        cena_koncowa = cena_koncowa_input_field.get()
        waluta_koncowa = waluta_koncowa_input_field.get()
        cennik = add_option_menu_value.get()

        waluta = str(waluta).upper()
        waluta_koncowa = str(waluta_koncowa).upper()
        cena_katalogowa = cena_katalogowa.replace(",", ".")

        if cena_koncowa is "":
            cena_koncowa = cena_katalogowa

        if waluta_koncowa is "":
            waluta_koncowa = waluta

        if kod_towaru is "" or kontrahent_kod is "" or kontrahent_cennik is "":
            show_info_label_for_add_window("WYPEŁNIJ BRAKUJĄCE POLA!")
        else:

            try:
                cena_katalogowa = float(cena_katalogowa)
            except ValueError:
                pass

            if isinstance(cena_katalogowa, str):
                show_info_label_for_add_window("Błędny format CENY!!! POPPRAW CENĘ")

            else:
                currencies = ['CHF', 'EUR', 'HUF', 'RON', 'USD']
                if waluta not in currencies or waluta_koncowa not in currencies:
                    show_info_label_for_add_window("OBSŁUGIWANE WALUTY:\nCHF EUR HUF RON USD ")

                else:
                    sql: str = "INSERT INTO " + "`" + "{}".format(cennik) + "`" \
                               + "(kodTowaru, kontrahentKod, kontrahentCennik, opis, cenaKatalogowa, " \
                                 "walutaKatalogowa, cenaKoncowa, walutaKoncowa )" \
                               + " VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(
                        kod_towaru, kontrahent_kod, kontrahent_cennik, opis,
                        cena_katalogowa, waluta, cena_koncowa, waluta_koncowa)
                    try:
                        cursor.execute(sql)
                        database.commit()
                        add_window_info_label = set_label(add_window_bottom_field,
                                                          "POMYŚLNIE DODANO {} DO BAZY DANYCH!!".format(kod_towaru),
                                                          0, 0, '#c7d4d1')
                        kod_towaru_input_field.delete(0, 'end')
                        kontrahent_input_field.delete(0, 'end')
                        kontrahent_cenni_input_field.delete(0, 'end')
                        opis_input_field.delete(0, 'end')
                        cena_katalogowa_input_field.delete(0, 'end')
                        waluta_input_field.delete(0, 'end')
                        cena_koncowa_input_field.delete(0, 'end')
                        waluta_koncowa_input_field.delete(0, 'end')
                        kod_towaru_input_field.focus_set()
                        add_window.after(3000, add_window_info_label.destroy)

                    except pymysql.err.IntegrityError:
                        show_info_label_for_add_window("DUPLIKAT")
                        database.rollback()


def click_add_data_to_database():
    add_data_to_database()


def close_app():
    if database is not None:
        disconnect_from_database(database)
    add_window.destroy()
    main_window.destroy()
    exit(0)


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def show_info_label_for_add_window(text):
    label = set_label(add_window_bottom_field, text, 0, 0, '#c7d4d1')
    add_window.after(3000, label.destroy)


# main

main_window = window.set_window('CENNIK', 1100, 550, '#c6c3c0')

icon = tk.PhotoImage(file='img/indeks.png')
main_window.tk.call('wm', 'iconphoto', main_window._w, icon)
main_window.protocol("WM_DELETE_WINDOW", close_app)

top_field = tk.Frame(main_window)
top_field.pack(side=tk.TOP, fill=tk.Y)
top_field.configure(background='#c6c3c0')

entry_and_button_field = tk.Frame(main_window)
entry_and_button_field.pack(side=tk.TOP, fill=tk.Y)
entry_and_button_field.configure(background='#c6c3c0')

result_field = tk.Frame(main_window)
result_field.pack(side=tk.TOP, fill=tk.Y)
result_field.configure(background='#c6c3c0')

bottom_field = tk.Frame(main_window)
bottom_field.pack(side=tk.TOP, fill=tk.Y)
bottom_field.configure(background='#c6c3c0')

multiple_input_field = set_multiple_input_field(entry_and_button_field, 0, 2, 0, tk.RAISED, 32, 5)
multiple_input_field.bind('<Control-Return>', press_enter_to_perform_multiple_search)
multiple_input_field.focus_set()

clear_input_field_img = tk.PhotoImage(file='img/clear_input_field.png')
clear_input_field_button = button.set_button_with_img(entry_and_button_field, 30, 30, clear_input_field_img,
                                                      clear_multiple_input_field, 0, 5, 1)
clear_input_field_button.grid(sticky=tk.N)

clear_multiple_input_field_button_tip = Create_tool_tip(clear_input_field_button, 'Wyczyść pole wprowadzania',
                                                        '#4D4D4D', '#c6c3c0')

sum_field_label = set_label(bottom_field, 'SUMA [€]: ', 0, 0, '#c6c3c0')
sum_field_label.grid(sticky=tk.N)

sum_field = set_label(bottom_field, "            ", 0, 1, 'white')
sum_field.grid(sticky=tk.N)

result_table: Treeview = define_result_table(result_field, "extended", (
    "kodTowaru", "kontrahent", "cennik", "cenaKoncowa", "cenaKatalogowa", "Rabat", "cenaKoncowaEUR", "zDnia"),
                                             "Custom.Treeview", 12)

scrollbar = tk.Scrollbar(result_field, orient="vertical", command=result_table.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_table.configure(yscrollcommand=scrollbar.set)
search_text_label = set_label(entry_and_button_field, 'Podaj kod Towaru: ', 0, 0, '#c6c3c0')
search_text_label.grid(sticky=tk.N)

info_label_img = tk.PhotoImage(file='img/info.png')
info_label = tk.Label(entry_and_button_field, image=info_label_img, height=20, width=20)
info_label.grid(row=0, column=1, sticky=tk.N, padx=4)
info_label.configure(background='#c6c3c0')
info_label_tip = Create_tool_tip(info_label,
                                 "CLR + V aby wkleić \n"
                                 "CTRL + ENTER aby wyszukać ")

search_button_img = tk.PhotoImage(file='img/multiple_search_img.png')
search_button = button.set_button_with_img(entry_and_button_field, 30, 30, search_button_img,
                                           click_search_button, 0,
                                           3, 1)
search_button.grid(sticky=tk.W)
search_button_tip = Create_tool_tip(search_button, 'WYSZUKAJ', "aqua")
search_button.grid(sticky=tk.N)

lowest_price_search_img = tk.PhotoImage(file='img/lowest_price.png')
lowest_price_search_button = button.set_button_with_img(entry_and_button_field, 30, 30, lowest_price_search_img,
                                                        show_only_lowest_prices, 0, 4, 1)
lowest_price_search_button.grid(sticky=tk.N)
lowest_price_search_button_tip = Create_tool_tip(lowest_price_search_button, 'WYSZUKAJ TYLKO NAJNIŻSZE CENY', 'black',
                                                 'white')

clear_button_img = tk.PhotoImage(file='img/clear_all.png')
clear_button = button.set_button_with_img(bottom_field, 20, 20, clear_button_img, click_clear_results, 0, 2, 1)
clear_button.config(state=tk.DISABLED)
clear_button_tip = Create_tool_tip(clear_button, 'Wyczyść wyszukiwania', 'black', '#c6c3c0')

export_img = tk.PhotoImage(file='img/Excel-icon.png')
export_button = button.set_button_with_img(bottom_field, 20, 20, export_img, click_export, 0, 3, 1)
export_button.config(state=tk.DISABLED)
export_button.grid(sticky=tk.N)
export_button_tip = Create_tool_tip(export_button, "Export do EXCELA", '#1D7044', 'white')


add_data_button_img = tk.PhotoImage(file='img/database.png')
add_data_button = button.set_button_with_img(bottom_field, 20, 20, add_data_button_img, open_add_window, 0, 5)
add_data_button_tip = Create_tool_tip(add_data_button, "Dodaj produkt do bazy", "#42C0FB", "white")
restart_button_img = tk.PhotoImage(file='img/restart.png')
restart_program_button = button.set_button_with_img(entry_and_button_field, 30, 30,
                                                    restart_button_img, restart_program, 0, 7)
restart_program_button.grid(sticky=tk.N)
restart_button_tip = Create_tool_tip(restart_program_button, 'Odśwież połączenie')


# table with query results
set_result_table(result_table)
result_table.pack(side=tk.LEFT, fill=tk.X)

# style of table
result_table_style = ttk.Style(result_field)
result_table_style.theme_use("clam")
result_table_style.configure("Treeview", background="#FFE4C4",
                             fieldbackground="#FFE4C4", foreground="black")

# table colors for different search
result_table.tag_configure('oddrow', background='#FFDAB9')
result_table.tag_configure('evenrow', background='#FFEBCA')
result_table.tag_configure('empty', background='lightcoral')

# add window
add_window = top_window.set_window("...::: WPROWADŹ DANE :::...", 380, 250, '#c7d4d1')

add_window.withdraw()
add_window.protocol("WM_DELETE_WINDOW", close_add_window)

add_window_middle_field = tk.Frame(add_window)
add_window_middle_field.grid(sticky=tk.N)
add_window_middle_field.configure(bg='#c7d4d1')

add_window_bottom_field = tk.Frame(add_window)
add_window_bottom_field.grid(sticky=tk.N)
add_window_bottom_field.configure(bg='#c7d4d1')


kod_towaru_Label = set_label(add_window_middle_field, "KOD TOWARU", 2, 1, '#c7d4d1')
kod_towaru_input_field = set_input_field(add_window_middle_field, 2, 2, 2, tk.SUNKEN, 31)

kontrahent_kod_Label = set_label(add_window_middle_field, "KONTRAHENT KOD", 3, 1, '#c7d4d1')
kontrahent_input_field = set_input_field(add_window_middle_field, 3, 2, 2, tk.SUNKEN, 31)

kontrahent_cennik_Label = set_label(add_window_middle_field, "KONTRAHENT CENNIK", 4, 1, '#c7d4d1')
kontrahent_cenni_input_field = set_input_field(add_window_middle_field, 4, 2, 2, tk.SUNKEN, 31)

opis_Label = set_label(add_window_middle_field, "OPIS", 5, 1, '#c7d4d1')
opis_input_field = set_input_field(add_window_middle_field, 5, 2, 2, tk.SUNKEN, 31)

cena_katalogowa_Label = set_label(add_window_middle_field, "CENA KATALOGOWA", 6, 1, '#c7d4d1')
cena_katalogowa_input_field = set_input_field(add_window_middle_field, 6, 2, 2, tk.SUNKEN, 31)

waluta_katalogowa_Label = set_label(add_window_middle_field, "WALUTA", 7, 1, '#c7d4d1')
waluta_input_field = set_input_field(add_window_middle_field, 7, 2, 2, tk.SUNKEN, 31)
waluta_input_field_tip = Create_tool_tip(waluta_input_field, 'CHF,EUR,HUF,RON,USD')

cena_koncowa_Label = set_label(add_window_middle_field, "CENA KOńCOWA", 8, 1, '#c7d4d1')
cena_koncowa_input_field = set_input_field(add_window_middle_field, 8, 2, 2, tk.SUNKEN, 31)

waluta_koncowa_Label = set_label(add_window_middle_field, "WALUTA KOńCOWA", 9, 1, '#c7d4d1')
waluta_koncowa_input_field = set_input_field(add_window_middle_field, 9, 2, 2, tk.SUNKEN, 31)

wybierz_cenik_Label = set_label(add_window_middle_field, "WYBIERZ CENNIK", 10, 1, '#c7d4d1')


save_data_button_img = tk.PhotoImage(file='img/add_button.png')
save_data_button = button.set_button_with_img(add_window_middle_field, 20, 20,
                                              save_data_button_img, click_add_data_to_database, 10, 3, 2)
save_data_button_tip = Create_tool_tip(save_data_button, "DODAJ DO BAZY", "#0166FF", "white")

database = connect_to_database('b2b.int-technics.pl', 'b2b_roboczy', 'b2b_roboczy', 'b2b_robocza')

if database is None:
    option_menu_value = tk.StringVar(top_field)
    option_menu_value.set("WYBÓR CENNIKA")
    tables_list = tk.OptionMenu(top_field, option_menu_value, *['Cennik 1', 'Cennik 2'])
    tables_list.grid(row=0, column=3, padx=5, sticky=tk.N)
    tables_list.config(width=35)
    tables_list_main_window_tip = Create_tool_tip(tables_list, 'Wybierz cennik', 'yellow')

    add_option_menu_value = tk.StringVar(add_window_bottom_field)
    add_option_menu_value.set("Wybór Tabeli")
    tables_list_add_window = tk.OptionMenu(add_window_middle_field, add_option_menu_value, *['TABELA1', 'TABELA1', ])
    tables_list_add_window.grid(row=10, column=2, padx=2, sticky=tk.N)
    tables_list_add_window_tip = Create_tool_tip(tables_list_add_window, 'Wybierz Tabele', 'yellow')

else:
    option_menu_value = tk.StringVar(top_field)
    option_menu_value.set(get_tables_list()[0])
    tables_list = tk.OptionMenu(top_field, option_menu_value, *get_tables_list())
    tables_list.grid(row=0, column=3, padx=2, sticky=tk.N)
    tables_list.config(width=35)
    tables_list_main_window_tip = Create_tool_tip(tables_list, 'Wybierz cennik', 'yellow')

    add_option_menu_value = tk.StringVar(add_window_bottom_field)
    add_option_menu_value.set(get_tables_list_to_add_data()[0])
    tables_list_add_window = tk.OptionMenu(add_window_middle_field,
                                           add_option_menu_value, *get_tables_list_to_add_data())
    tables_list_add_window.grid(row=10, column=2, padx=5, sticky=tk.N)
    tables_list_add_window_add_window_tip = Create_tool_tip(tables_list_add_window, 'Wybierz Tabele', 'yellow')
    tables_list_add_window.config(width=25)

main_window.mainloop()
