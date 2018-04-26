import tkinter as tk
import tkinter.ttk

import pymysql


window_1 = tk.Tk()
window_1.maxsize(width=1280, height=720)
window_1.minsize(width=1280, height=720)
window_1.title('CENNIKI')
resultTable = tkinter.ttk.Treeview(window_1)



database = pymysql.connect('b2b.int-technics.pl', 'b2b_roboczy', 'b2b_roboczy', 'b2b_robocza')

cursor = database.cursor()

def clickSearchButton():

    kodTowaru = inputField_1.get()

    sql = "SELECT * FROM "+"`"+optionMenuValue.get()+"`"+ " WHERE kodTowaru = '{}'".format(kodTowaru)

    cursor.execute(sql)

    results = cursor.fetchall()
    outputField.config(state=tk.NORMAL)

    try:
        for row in results:

            kontrahent = row[1]
            kontrahentCennik = row[2]
            cenaKoncowa = row[7]
            cenaKatalogowaEUR = row[8]
            rabat= row[10]
            zDnia = row[11]
            cenaKonEUR = row[9]

            cenaKatalogowaEUR = round(cenaKatalogowaEUR,2)
            cenaKonEUR = round(cenaKonEUR,2)
            rabat = round(rabat,2)

            product= []
            product.append(kontrahent)
            product.append(kontrahentCennik)
            product.append(cenaKoncowa)
            product.append(cenaKatalogowaEUR)
            product.append(rabat)
            product.append(zDnia)
            product.append(cenaKonEUR)




            outputField.insert(tk.INSERT,product)
            # outputKontrahent.insert(tk.INSERT,product[0])
            # outputKontrahent.insert(tk.END, '\n')
            outputField.insert(tk.END, '\n')
            outputField.insert(tk.END, '______________________________________________________________________\n')
            resultTable.insert("", 0, values=(kontrahent, kontrahentCennik, cenaKoncowa, cenaKatalogowaEUR, rabat, cenaKonEUR, zDnia))




    #kontrola
    except:
        print('NIE ZNALEZIONO')
    outputField.config(state=tk.DISABLED)




def clickClearResults():
    outputField.config(state=tk.NORMAL)
    outputField.delete('1.0', tk.END)
    for i in resultTable.get_children():
        resultTable.delete(i)


def getTablesList():
    cursor = database.cursor()

    cursor.execute("SHOW TABLES in b2b_robocza LIKE 'zestaw%' ")

    tables = cursor.fetchall()
    getTables_list = []
    for (table_name,) in tables:
        getTables_list.append(table_name)

    return getTables_list





resultTable["columns"] = ("kontrahent", "cennik", "cenaKoncowa", "cenaKatalogowa", "Rabat", "cenaKoncowaEUR", "zDnia")
resultTable.column("kontrahent", width=100)
resultTable.column("cennik", width=100)
resultTable.column("cenaKoncowa", width=100)
resultTable.column("cenaKatalogowa", width=100)
resultTable.column("Rabat", width=100)
resultTable.column("cenaKoncowaEUR", width=100)
resultTable.column("zDnia", width=100)
resultTable.heading("kontrahent", text="kontrahent")
resultTable.heading("cennik", text="cennik")
resultTable.heading("cenaKoncowa", text="cenaKoncowa")
resultTable.heading("cenaKatalogowa", text="cenaKatalogowa")
resultTable.heading("Rabat", text="Rabat")
resultTable.heading("cenaKoncowaEUR", text="cenaKoncowaEUR")
resultTable.heading("zDnia", text="zDnia")









resultTable.grid(row=0, column=0)

searchButton = tk.Button(window_1, text='WYSZUKAJ', command=clickSearchButton)
searchButton.grid(row=5, column=0)

clearButton = tk.Button(window_1, text='WYCZYŚć WYSZUKIWANE', command=clickClearResults)
clearButton.grid(row=7, column=0)

searchTextField = tk.Label(window_1, text='Podaj kod Towaru: ')
searchTextField.grid(row=1,column=0)

inputField_1 = tk.Entry(window_1)

inputField_1.grid(row=2, column=0)
inputField_1.focus()

outputField = tk.Text()

outputField.grid(row=8, column=0)
outputField.config(state=tk.DISABLED)

scrollbar = tk.Scrollbar(window_1, command=outputField.yview)
#scrollbar.grid(row=1, column=5, sticky=tk.N)

scrollbar.size()
outputField['yscrollcommand'] = scrollbar.set

optionMenuValue = tk.StringVar(window_1)
optionMenuValue.set("WYBIERZ CENNIK")

tables_list = tk.OptionMenu(window_1, optionMenuValue, *getTablesList())

# tables_list.pack()
tables_list.grid(row=3, column=0, rowspan=2, sticky=tk.N)

# outputKontrahent=tk.Text()
# outputKontrahent.grid(row=0, column=1, columnspan=2, rowspan=2,
#                       sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)
#
# outputCennik=tk.Text()
# outputCennik.grid(row=0,column=3)

window_1.mainloop()
