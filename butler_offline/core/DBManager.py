'''
Read panda files
'''

from _io import StringIO
from datetime import datetime
from butler_offline.core import DatabaseModule
from butler_offline.core import FileSystem
import pandas as pd

def read(nutzername, ausgeschlossene_kategorien):
    if not FileSystem.instance().read(database_path_from(nutzername)):
        neue_datenbank = DatabaseModule.Database(nutzername)
        write(neue_datenbank)

    file_content = FileSystem.instance().read(database_path_from(nutzername))

    reader = MultiPartCsvReader(
            set(['Einzelbuchungen', 'Dauerauftraege', 'Gemeinsame Buchungen']),
            'Einzelbuchungen')
    reader.from_string(file_content)

    database = DatabaseModule.Database(nutzername, ausgeschlossene_kategorien=ausgeschlossene_kategorien)

    raw_data = pd.read_csv(StringIO(reader.get_string('Einzelbuchungen')))
    database.einzelbuchungen.parse(raw_data)
    print("READER: Einzelbuchungen gelesen")

    database.dauerauftraege.parse(pd.read_csv(StringIO(reader.get_string('Dauerauftraege'))))
    print("READER: Daueraufträge gelesen")

    database.gemeinsamebuchungen.parse(pd.read_csv(StringIO(reader.get_string('Gemeinsame Buchungen'))))
    print("READER: Gemeinsame Buchungen gelesen")

    print('READER: Refreshe Database')
    database.refresh()
    print('READER: Refresh done')
    return database

def write(database):
    einzelbuchungen = database.einzelbuchungen.content.copy()[database.einzelbuchungen.content.Dynamisch == False]
    einzelbuchungen_raw_data = einzelbuchungen[['Datum', 'Kategorie', 'Name', 'Wert', 'Tags']]
    content = einzelbuchungen_raw_data.to_csv(index=False)

    content += "\n Dauerauftraege \n"
    content += database.dauerauftraege.content.to_csv(index=False)

    content += "\n Gemeinsame Buchungen \n"
    content += database.gemeinsamebuchungen.content.to_csv(index=False)

    FileSystem.instance().write(database_path_from(database.name), content)
    print("WRITER: All Saved")



def database_path_from(username):
    return '../Database_' + username + '.csv'

class MultiPartCsvReader:

    def __init__(self, token, start_token):
        self._token = token
        self._start_token = start_token
        self._tables = {}

    def from_string(self, lines):
        self._tables = dict.fromkeys(self._token, '')
        mode = self._start_token

        for line in lines:
            line = line.strip()
            if line == "":
                continue

            if line in self._token:
                mode = line
                continue

            if not ',' in line:
                break

            self._tables[mode] = self._tables[mode] + "\n" + line

    def get_string(self, token):
        return self._tables[token].strip()
