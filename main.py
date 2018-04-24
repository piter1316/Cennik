import tkinter as tk
import pymysql

database = pymysql.connect('b2b.int-technics.pl', 'b2b_roboczy', 'b2b_roboczy', 'b2b_robocza')
cursor = database.cursor()
tables = ['__OMRON_Cennik','__PILZ_Cennik_copy','__ABB_Cennik','__ALLEN-BRADLEY_Cennik']





def clickSearchButton():


    kodTowaru = inputField_1.get()

    sql = "SELECT * FROM __PILZ_Cennik_copy WHERE kodTowaru = '{}'".format(kodTowaru)

    cursor.execute(sql)

    results = cursor.fetchall()
    try:
        for row in results:

            kontrahent = row[1]
            kontrahentCennik = row[2]
            cenaKatalogowa = row[7]
            walutaKatalogowa = row[8]

            product= []
            product.append(kontrahent)
            product.append(kontrahentCennik)
            product.append(cenaKatalogowa)
            product.append(walutaKatalogowa)
            print(product)
            outputField.insert(tk.INSERT,product)
            outputField.insert(tk.END, '\n')



    #kontrola
    except:
        print('NIE ZNALEZIONO')


def clickClearResults():
    outputField.delete('1.0', tk.END)

def getTables(tab):
    for i in range (len(tab)):
        return(tables[i])


window_1 = tk.Tk()
window_1.maxsize(width=1280, height=720)
window_1.minsize(width=1280, height=720)
window_1.title('CENNIKI')

searchButton = tk.Button(window_1, text='WYSZUKAJ', command=clickSearchButton)
searchButton.pack(side=tk.TOP)

clearButton = tk.Button(window_1, text='WYCZYŚć WYSZUKIWANE', command=clickClearResults)
clearButton.pack(side=tk.TOP)

searchTextField = tk.Label(window_1, text='Podaj kodTowaru: ')
searchTextField.pack(side=tk.TOP)

inputField_1 = tk.Entry(window_1)
inputField_1.place(x=150, y=10)
inputField_1.pack(side=tk.TOP)
inputField_1.focus()

outputField = tk.Text()
outputField.place(x=150, y=150)
outputField.pack(side=tk.TOP)

var = tk.StringVar(window_1)
default = tables[0]

tables_list = tk.OptionMenu(window_1,var,*tables)



tables_list.pack()
tables_list.place(x=20,y=20)

print(getTables(tables))
window_1.mainloop()

