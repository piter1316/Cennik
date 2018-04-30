import tkinter as tk
import xlsxwriter
from tkinter import messagebox
import tkinter.ttk
import pymysql
#global dabase
data = []


def connectToDatabase(url,user,password,dataBaseName):
    database = pymysql.connect(url,user,password,dataBaseName)
    global cursor
    cursor= database.cursor()
    return database
def disconectFromDatabase(database):
    database.close()

def defineResultTable(frame,mode,columns):
    table = tkinter.ttk.Treeview(frame,selectmode=mode,columns=columns)
    return table

def setResultTable(resultTable):
    resultTable.heading("kodTowaru",text="kod")
    resultTable.column("kodTowaru", width=130)

    resultTable.heading("kontrahent", text="kontrahent")
    resultTable.column("kontrahent", width=150)

    resultTable.heading("cennik", text="cennik")
    resultTable.column("cennik", width=80)

    resultTable.heading("cenaKoncowa", text="cenaKoncowa[wal]")
    resultTable.column("cenaKoncowa", width=110)

    resultTable.heading("cenaKatalogowa", text="cenaKatalogowa[€]")
    resultTable.column("cenaKatalogowa", width=110)

    resultTable.heading("Rabat", text="Rabat")
    resultTable.column("Rabat", width=50)

    resultTable.heading("cenaKoncowaEUR", text="cenaKoncowa[€]")
    resultTable.column("cenaKoncowaEUR", width=110)

    resultTable.heading("zDnia", text="zDnia")
    resultTable.column("zDnia", width=80)

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

def fetchDataFromDatabase():
    try:
        cursor.execute(prepareSqlSelectQuery())

        results = cursor.fetchall()
    except:
        messagebox.showinfo("Błąd", "Podana Baza danych nie istnieje!")

    return results

def insertDataIntoTable():
    if len(fetchDataFromDatabase())>0:
        try:

            for row in fetchDataFromDatabase():
                kodTowaru = row[0]
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
                product.append(kodTowaru)
                product.append(kontrahent)
                product.append(kontrahentCennik)
                product.append(cenaKoncowa)
                product.append(cenaKatalogowaEUR)
                product.append(rabat)
                product.append(cenaKonEUR)
                product.append(zDnia)
                data.append(product)

                resultTable.insert("", "end", values=(kodTowaru,kontrahent, kontrahentCennik, cenaKoncowa, cenaKatalogowaEUR, rabat, cenaKonEUR, zDnia))
        except:
            messagebox.showinfo("Błąd POBIERANIA DANYCH")
    else:
        messagebox.showinfo("NIE ZNALEZIONO", "BRAK KODU W BAZIE")

def clickSearchButton():

    fetchDataFromDatabase()
    insertDataIntoTable()

def clickClearResults():
    for i in resultTable.get_children():
        resultTable.delete(i)

def exportToXls(data):

    workbook = xlsxwriter.Workbook('arrays.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0,0,["kodTowaru","kontrahent", "cennik", "cenaKoncowa", "cenaKatalogowa_EUR", "Rabat", "cenaKoncowaEUR", "zDnia"])
    row=0


    for col, data in enumerate(data):
        col = col + 1
        worksheet.write_row(col, row, data)
    workbook.close()

def clickExport():
    exportToXls(data)

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
window_1 = setWindow('CENNIK',1000,480)

database = connectToDatabase('b2b.int-technics.pl', 'b2b_roboczy', 'b2b_roboczy', 'b2b_robocza')

resultTable = defineResultTable(window_1,"extended",("kodTowaru","kontrahent", "cennik", "cenaKoncowa", "cenaKatalogowa", "Rabat", "cenaKoncowaEUR", "zDnia"))

setResultTable(resultTable)
showTable(resultTable,0,0)

searchButton = setButton(window_1,'WYSZUKAJ',clickSearchButton,5,0)

clearButton = setButton(window_1,"WYCZYŚć WYSZUKIWANIE",clickClearResults,6,0)

exportButton = setButton(window_1,"Export do pliku",clickExport,7,0)

searchTextLabel = setLabel(window_1, 'Podaj kod Towaru: ', 1, 0)

inputField_1 = setInputField(window_1,2,0)
inputField_1.focus()

scrollbar = tk.Scrollbar(window_1, command=resultTable.yview)
scrollbar.grid(row=0, column=2, sticky=tk.N)

optionMenuValue = tk.StringVar(window_1)
optionMenuValue.set(getTablesList()[0])

tables_list = tk.OptionMenu(window_1, optionMenuValue, *getTablesList())
tables_list.grid(row=3, column=0, rowspan=2, sticky=tk.N)

window_1.mainloop()
disconectFromDatabase(database)
