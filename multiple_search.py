from tkinter import messagebox
import main

from main import fetch_data_from_database, inputField_1, clear_results, data, result_table


def insert_multiple_search_into_table():

    global just_opened

    if len(main.multiple_input_field.get(0,'end')) == 0:
        messagebox.showinfo("Pusto", "PODAJ KOD!!!")
    elif len(fetch_data_from_database()) > 0:
        clear_results()

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

            result_table.insert("", "end", values=(
                kod_towaru, kontrahent, kontrahent_cennik, cena_koncowa, cena_katalogowa_eur, rabat,
                cena_kon_eur, z_dnia), tags='rowbg')

        inputField_1.delete(0, 'end')
        just_opened += 1

    else:

        messagebox.showerror("NIE ZNALEZIONO", "BRAK KODU W BAZIE")
