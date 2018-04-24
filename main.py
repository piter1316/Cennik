import tkinter as tk
import pymysql
database = pymysql.connect('b2b.int-technics.pl', 'b2b_roboczy', 'b2b_roboczy', 'b2b_robocza')
cursor = database.cursor()

def clickSearchButton():
    kodTowaru = inputField_1.get()


    sql = "SELECT * FROM __PILZ_Cennik_copy WHERE kodTowaru = '{}'".format(kodTowaru)

    cursor.execute(sql)

    results = cursor.fetchall()
    try:
        for row in results:
            kod = row[0]
            kontrahent = row[1]
            cenaKatalogowa = row[7]
            walutaKatalogowa = row[8]
            print(kod, kontrahent, cenaKatalogowa, walutaKatalogowa)
    except:
        print('NIE ZNALEZIONO')

window_1 = tk.Tk()
window_1.maxsize(width=1280,height=720)
window_1.minsize(width=1280,height=720)

searchButton = tk.Button(window_1, text='WYSZUKAJ',command=clickSearchButton)
#searchButton.place(x=10, y=10)
searchButton.pack(side=tk.TOP)

searchTextField = tk.Label(window_1, text='Podaj kodTowaru: ')
searchTextField.place(x=10,y=10)
inputField_1= tk.Entry(window_1)
inputField_1.place(x=150,y=10)
inputField_1.focus()

window_1.mainloop()


