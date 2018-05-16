import tkinter as tk
from tkinter import filedialog


def klik_przycisk_print():
    tekst = pole_tekstowe.get("1.0", tk.END)
    print(tekst)


def klik_czysc():
    pole_tekstowe.delete("1.0", tk.END)


def zapisz_na_liste():
    tekst = tekst = pole_tekstowe.get("1.0", tk.END)
    lista = []
    for line in tekst.splitlines():
        if line != "":
            lista.append(line)
    print(lista)
    return lista


def klik_zapisz_na_liste():
    zapisz_na_liste()


def zaznacz_wszystko():
    pole_tekstowe.tag_add(tk.SEL, "1.0", tk.END)


def kopiuj():
    okno.clipboard_clear()
    try:
        text = pole_tekstowe.get("sel.first", "sel.last")

        okno.clipboard_append(text)
    except:
        pass


def wklej():
    try:
        tekst = pole_tekstowe.selection_get(selection='CLIPBOARD')
        pole_tekstowe.insert('insert', tekst)
    except:
        pass


def wytnij():
    okno.clipboard_clear()
    try:
        tekst = pole_tekstowe.get("sel.first", "sel.last")
        okno.clipboard_append(tekst)
        pole_tekstowe.delete("sel.first", "sel.last")
    except:
        pass


def wyczysc_wszystko():
    pole_tekstowe.delete("1.0", tk.END)


def zapisz_jako():
    sciezka_zapisu = filedialog.asksaveasfilename(initialdir="/",
                                                  title="ZAPISZ JAKO",
                                                  filetypes=(("TEXT", "*.txt"), ("all files", "*.*")),
                                                  defaultextension='.txt')
    plik = open(sciezka_zapisu, "+w")
    plik.write(pole_tekstowe.get("1.0", tk.END))
    plik.close()


okno = tk.Tk()
okno.title("Nowe Okno")
width = 900
height = 450
okno.minsize(width=width, height=height)

sw = okno.winfo_screenwidth()
sh = okno.winfo_screenheight()
okno.configure(background='crimson')

x = sw / 2 - (width / 2)
y = sh / 2 - (height / 2)

okno.geometry('{}x{}+{}+{}'.format(width, height, int(x), int(y)))

pasek_menu = tk.Menu(okno)
plik_menu = tk.Menu(pasek_menu)
edycja_menu = tk.Menu(pasek_menu)

pasek_menu.add_cascade(label="PLIK", menu=plik_menu)
plik_menu.add_command(label="ZAPISZ JAKO", command=zapisz_jako)

pasek_menu.add_cascade(label="EDYCJA", menu=edycja_menu)

edycja_menu.add_command(label="WYTNIJ", command=wytnij)
edycja_menu.add_command(label="KOPIUJ", command=kopiuj)
edycja_menu.add_command(label="WKLEJ", command=wklej)
edycja_menu.add_command(label="ZAZNACZ WSZYSTKO", command=zaznacz_wszystko)
edycja_menu.add_command(label="WYCZYŚĆ WSZYSTKO", command=wyczysc_wszystko)
edycja_menu.add_command(label="WYJDŹ", command=exit)

okno.config(menu=pasek_menu)

pole_tekstowe = tk.Text(width=width)
pole_tekstowe.pack()

pole_przyciskow = tk.Frame()
pole_przyciskow.pack()

przycisk_print = tk.Button(pole_przyciskow, text="ODCZYT i PRINT", command=klik_przycisk_print)
przycisk_print.pack(side=tk.LEFT)

przycisk_czysc = tk.Button(pole_przyciskow, text="CZYŚĆ", command=klik_czysc)
przycisk_czysc.pack(side=tk.LEFT)

przycisk_zapisz_na_liste = tk.Button(pole_przyciskow, text="ZAPISZ DO LISTY", command=klik_zapisz_na_liste)
przycisk_zapisz_na_liste.pack(side=tk.LEFT)
