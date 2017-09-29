'''
Read panda files
'''

from _io import StringIO
from datetime import datetime
import os

from core import DatabaseModule
import pandas as pd





def read_database(nutzername):
    return read_function(nutzername)


def from_file(nutzername):
    if not os.path.isfile('../Database_' + nutzername + ".csv"):
        neue_datenbank = DatabaseModule.Database(nutzername)
        write(neue_datenbank)

    file = open('../Database_' + nutzername + ".csv", 'r')
    return read_file(file, nutzername)

def to_file(database):
    file = open('../Database_' + database.name + ".csv", 'w')
    write_file(database, file)
    file.close()


read_function = from_file
write_function = to_file

def read_file(file, nutzername):
    tables = {}

    tables["einzelbuchungen"] = ""
    tables["dauerauftraege"] = ""
    tables["gemeinsamebuchungen"] = ""
    tables["Stechzeiten"] = ""
    tables["Sollzeiten"] = ""
    tables["Sonderzeiten"] = ""
    mode = "einzelbuchungen"
    for line in file:
        line = line.strip()
        if line == "":
            continue
        if line == 'Dauerauftraege':
            mode = 'dauerauftraege'
            continue

        if line == 'Gemeinsame Buchungen':
            mode = 'gemeinsamebuchungen'
            continue

        if line == 'Stechzeiten':
            mode = 'Stechzeiten'
            continue

        if line == 'Sollzeiten':
            mode = 'Sollzeiten'
            continue

        if line == 'Sonderzeiten':
            mode = 'Sonderzeiten'
            continue

        tables[mode] = tables[mode] + "\n" + line


    database = DatabaseModule.Database(nutzername)

    raw_data = pd.read_csv(StringIO(tables["einzelbuchungen"]))
    database.einzelbuchungen.parse(raw_data)
    print("READER: Einzelbuchungen gelesen")

    database.dauerauftraege.parse(pd.read_csv(StringIO(tables["dauerauftraege"])))
    print("READER: Daueraufträge gelesen")

    database.gemeinsamebuchungen.parse(pd.read_csv(StringIO(tables["gemeinsamebuchungen"])))

    if tables['Stechzeiten'] != "":
        database.stechzeiten.parse(pd.read_csv(StringIO(tables["Stechzeiten"])))

    if tables['Sollzeiten'] != "":
        database.sollzeiten.parse(pd.read_csv(StringIO(tables["Sollzeiten"])))

    if tables['Sonderzeiten'] != "":
        database.sonderzeiten.parse(pd.read_csv(StringIO(tables["Sonderzeiten"])))



    print('READER: Refreshe Database')
    database.refresh()
    print('READER: Refresh done')
    return database

def write(database):
    write_function(database)

def write_file(database, file):
    einzelbuchungen = database.einzelbuchungen.content.copy()[database.einzelbuchungen.content.Dynamisch == False]
    einzelbuchungen_raw_data = einzelbuchungen[['Datum', 'Kategorie', 'Name', 'Wert', 'Tags']]
    content = einzelbuchungen_raw_data.to_csv(index=False)

    content += "\n Dauerauftraege \n"
    content += database.dauerauftraege.content.to_csv(index=False)

    content += "\n Gemeinsame Buchungen \n"
    content += database.gemeinsamebuchungen.content.to_csv(index=False)

    content += "\n Stechzeiten \n"
    content += database.stechzeiten.content[database.stechzeiten.persitent_stechzeiten_columns].to_csv(index=False)

    content += "\n Sollzeiten \n"
    content += database.sollzeiten.content.to_csv(index=False)

    content += "\n Sonderzeiten \n"
    content += database.sonderzeiten.content.to_csv(index=False)

    file.write(content)

    print("WRITER: All Saved")

def export(database):
    '''
    writes the DATABASE into a file
    '''
    path = "./" + database.name + "_Export_" + str(datetime.today())
    einzelbuchungen_raw_data = database.einzelbuchungen.content.copy()[['Datum', 'Kategorie', 'Name', 'Wert', 'Tags']]
    einzelbuchungen_raw_data.to_csv(path, index=False)
    print("WRITER: Exportiere in : ", path)
    print("WRITER: Export Data:")
    print(einzelbuchungen_raw_data)
    print("WRITER: Done")
