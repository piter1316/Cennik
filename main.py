import tkinter as tk
import pymysql

database = pymysql.connect('b2b.int-technics.pl', 'b2b_roboczy', 'b2b_roboczy', 'b2b_robocza')
cursor = database.cursor()


def clickSearchButton():
    global product

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

            product= []
            product.append(kod)
            product.append(kontrahent)
            product.append(cenaKatalogowa)
            product.append(walutaKatalogowa)
            print(product)
            outputField.insert(tk.INSERT,product)
            outputField.insert(tk.END, "\n")


    except:
        print('NIE ZNALEZIONO')
def clickClearResults():
    outputField.delete('1.0', tk.END)
window_1 = tk.Tk()
window_1.maxsize(width=1280, height=720)
window_1.minsize(width=1280, height=720)

searchButton = tk.Button(window_1, text='WYSZUKAJ', command=clickSearchButton)
# searchButton.place(x=10, y=10)
searchButton.pack(side=tk.TOP)

clearButton = tk.Button(window_1, text='WYCZYŚć WYSZYKIWANE', command=clickClearResults)
# searchButton.place(x=10, y=10)
clearButton.pack(side=tk.TOP)

searchTextField = tk.Label(window_1, text='Podaj kodTowaru: ')
searchTextField.place(x=10, y=10)
inputField_1 = tk.Entry(window_1)
inputField_1.place(x=150, y=10)
inputField_1.focus()

outputField = tk.Text()
outputField.place(x=150, y=150)





window_1.mainloop()
