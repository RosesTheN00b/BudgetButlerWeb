from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd


class Order(DatabaseObject):
    TABLE_HEADER = ['Datum', 'Name', 'Konto', 'Depotwert', 'Wert']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)

    def add(self, datum, name, konto, depotwert, wert):
        neue_order = pd.DataFrame([[datum, name, konto, depotwert, wert]], columns=self.TABLE_HEADER)
        self.content = self.content.append(neue_order, ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self):
        return self.content

    def edit(self, index, datum, name, konto, depotwert, wert):
        self.edit_element(index, {
            'Datum': datum,
            'Name': name,
            'Konto': konto,
            'Depotwert': depotwert,
            'Wert': wert
        })

    def _sort(self):
        self.content = self.content.sort_values(by=['Datum', 'Konto', 'Name'])
        self.content = self.content.reset_index(drop=True)
