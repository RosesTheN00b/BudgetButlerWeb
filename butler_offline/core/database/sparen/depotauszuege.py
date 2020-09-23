from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd
import numpy as np

class Depotauszuege(DatabaseObject):
    TABLE_HEADER = ['Datum', 'Depotwert', 'Konto', 'Wert']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)


    def add(self, datum, depotwert, konto, wert):
        neuer_auszug = pd.DataFrame([[datum, depotwert, konto, wert]], columns=self.TABLE_HEADER)
        self.content = self.content.append(neuer_auszug, ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self):
        return self.content

    def edit(self, index, datum, depotwert, konto, wert):
        self.edit_element(index, {
            'Datum': datum,
            'Depotwert': depotwert,
            'Konto': konto,
            'Wert': wert
        })

    def get_by(self, datum, konto):
        auszuege = self.content[self.content.Konto == konto].copy()
        auszuege = auszuege[auszuege.Datum == datum]
        return auszuege

    def get_latest_datum_by(self, konto):
        auszuege = self.content[self.content.Konto == konto].copy()
        if len(auszuege) == 0:
            return None
        return auszuege.Datum.max()

    def resolve_index(self, datum, konto, depotwert):
        auszuege = self.get_by(datum, konto)
        result_frame = auszuege[auszuege.Depotwert == depotwert]
        if len(result_frame) == 0:
            return None
        return result_frame.index[0]

    def _sort(self):
        self.content = self.content.sort_values(by=['Datum', 'Konto', 'Depotwert'])
        self.content = self.content.reset_index(drop=True)