import tkinter as tk
import pymysql

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

            product= []
            product.append(kontrahent)
            product.append(kontrahentCennik)
            product.append(cenaKoncowa)
            product.append(cenaKatalogowaEUR)
            product.append(rabat)
            product.append(zDnia)

            outputField.insert(tk.INSERT,product)
            # outputKontrahent.insert(tk.INSERT,product[0])
            # outputKontrahent.insert(tk.END, '\n')
            outputField.insert(tk.END, '\n')
            outputField.insert(tk.END, '______________________________________________________________________\n')



    #kontrola
    except:
        print('NIE ZNALEZIONO')
    outputField.config(state=tk.DISABLED)




def clickClearResults():
    outputField.config(state=tk.NORMAL)
    outputField.delete('1.0', tk.END)

def getTablesList():
    cursor = database.cursor()

    cursor.execute("SHOW TABLES in b2b_robocza LIKE 'zestaw%' ")

    tables = cursor.fetchall()
    getTables_list = []
    for (table_name,) in tables:

        getTables_list.append(table_name)

    return getTables_list

window_1 = tk.Tk()
window_1.maxsize(width=1280, height=720)
window_1.minsize(width=1280, height=720)
window_1.title('CENNIKI')

searchButton = tk.Button(window_1, text='WYSZUKAJ', command=clickSearchButton)
searchButton.grid(row=0,column=6,sticky=tk.N)

clearButton = tk.Button(window_1, text='WYCZYŚć WYSZUKIWANE', command=clickClearResults)
clearButton.grid(row=0,column=7,sticky=tk.N)

searchTextField = tk.Label(window_1, text='Podaj kodTowaru: ')
searchTextField.grid(row=0,sticky=tk.W+tk.N)


inputField_1 = tk.Entry(window_1)

inputField_1.grid(row=0,column=1,sticky=tk.N)
inputField_1.focus()

outputField = tk.Text()
#outputField.place(x=150, y=150)
outputField.grid(row=0,column=4)
outputField.config(state=tk.DISABLED)

scrollbar = tk.Scrollbar(window_1,command=outputField.yview)
scrollbar.grid(row=0, column=5, sticky=tk.N)

scrollbar.size()
outputField['yscrollcommand'] = scrollbar.set

optionMenuValue = tk.StringVar(window_1)
optionMenuValue.set("WYBIERZ CENNIK")


tables_list = tk.OptionMenu(window_1,optionMenuValue,*getTablesList())

#tables_list.pack()
tables_list.grid(row=0,column=3,rowspan=2,sticky=tk.N)


# outputKontrahent=tk.Text()
# outputKontrahent.grid(row=0, column=1, columnspan=2, rowspan=2,
#                       sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)
#
# outputCennik=tk.Text()
# outputCennik.grid(row=0,column=3)

window_1.mainloop()






