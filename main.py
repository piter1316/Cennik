import tkinter as tk
from tkinter import messagebox
import tkinter.ttk
import pymysql

def connectToDatabase(url,user,password,dataBaseName):
    database = pymysql.connect(url,user,password,dataBaseName)
    global cursor
    cursor= database.cursor()
    return database
def defineResultTable(frame,mode,columns):
    table = tkinter.ttk.Treeview(frame,selectmode=mode,columns=columns)
    return table

def setResultTable(resultTable):
    resultTable.column("kontrahent", width=150)
    resultTable.column("cennik", width=80)
    resultTable.column("cenaKoncowa", width=100)
    resultTable.column("cenaKatalogowa", width=100)
    resultTable.column("Rabat", width=60)
    resultTable.column("cenaKoncowaEUR", width=110)
    resultTable.column("zDnia", width=80)
    resultTable.heading("kontrahent", text="kontrahent")
    resultTable.heading("cennik", text="cennik")
    resultTable.heading("cenaKoncowa", text="cenaKoncowa")
    resultTable.heading("cenaKatalogowa", text="cenaKatalogowa")
    resultTable.heading("Rabat", text="Rabat")
    resultTable.heading("cenaKoncowaEUR", text="cenaKoncowaEUR")
    resultTable.heading("zDnia", text="zDnia")
    resultTable['show'] = 'headings'
    return resultTable

def showTable(resultTable,row,column):
    resultTable.grid(row=row, column=column)

def prepareSqlSelectQuery():
    kodTowaru = str(inputField_1.get())
    kodTowaru = kodTowaru.replace('"', '')
    kodTowaru = kodTowaru.replace("'", "")
    kodTowaru = kodTowaru.replace("&", "")
    kodTowaru = kodTowaru.replace("<!--", "")
    kodTowaru = kodTowaru.replace("-->", "")
    kodTowaru = kodTowaru.replace(">", "")
    kodTowaru = kodTowaru.replace("<", "")
    kodTowaru = kodTowaru.replace("$", "")
    kodTowaru = kodTowaru.replace("\r", "")
    kodTowaru = kodTowaru.replace("!", "")

    sql = "SELECT * FROM " + "`" + optionMenuValue.get() + "`" + " WHERE kodTowaru = '{}'".format(kodTowaru)
    return sql

def clickSearchButton():

    try:
        cursor.execute(prepareSqlSelectQuery())

        results = cursor.fetchall()

        if len(results)>0:

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
                    resultTable.insert("", 1, values=(kontrahent, kontrahentCennik, cenaKoncowa, cenaKatalogowaEUR, rabat, cenaKonEUR, zDnia))

            except:
                messagebox.showinfo("Błąd POBIERANIA DANYCH")

                print('NIE ZNALEZIONO')
        else:
            messagebox.showinfo("NIE ZNALEZIONO", "BRAK KODU W BAZIE")
    except:
        messagebox.showinfo("Błąd","Podana Baza danych nie istnieje!")

def clickClearResults():
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

def setButton(frame,text,command,row,column):
    button = tk.Button(frame, text=text, command=command)
    button.grid(row=row,column=column)
    return button

def setLabel(frame,text,row,column):
    label =  tk.Label(frame, text=text)
    label.grid(row=row,column=column)
    return label

def setWindow(title, width, height):
    window = tk.Tk()
    window.maxsize(width=width, height=height)
    window.minsize(width=width, height=height)
    window.title(title)
    return window

def setInputField(frame,row,column):
    field = tk.Entry(frame)
    field.grid(row=row, column=column)
    return field


#main
window_1 = setWindow('CENNIK',720,480)

database = connectToDatabase('b2b.int-technics.pl', 'b2b_roboczy', 'b2b_roboczy', 'b2b_robocza')

resultTable = defineResultTable(window_1,"extended",("kontrahent", "cennik", "cenaKoncowa", "cenaKatalogowa", "Rabat", "cenaKoncowaEUR", "zDnia"))

setResultTable(resultTable)
showTable(resultTable,0,0)

searchButton = setButton(window_1,'WYSZUKAJ',clickSearchButton,5,0)

clearButton = setButton(window_1,"WYCZYŚć WYSZUKIWANIE",clickClearResults,6,0)

searchTextLabel = setLabel(window_1, 'Podaj kod Towaru: ', 1, 0)

inputField_1 = setInputField(window_1,2,0) #tk.Entry(window_1)
inputField_1.focus()

scrollbar = tk.Scrollbar(window_1, command=resultTable.yview)
scrollbar.grid(row=0, column=2, sticky=tk.N)

optionMenuValue = tk.StringVar(window_1)
optionMenuValue.set(getTablesList()[0])

tables_list = tk.OptionMenu(window_1, optionMenuValue, *getTablesList())
tables_list.grid(row=3, column=0, rowspan=2, sticky=tk.N)

window_1.mainloop()
