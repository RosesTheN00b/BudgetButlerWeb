import unittest
import numpy as np
import datetime

from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.core import file_system
from butler_offline.views import import_data
from butler_offline.views import configuration
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import request_handler
from butler_offline.viewcore import configuration_provider
from butler_offline.viewcore.viewcore import database_instance
from butler_offline.viewcore import requester
from butler_offline.test.RequesterStub import RequesterStub, MockedResponse
from butler_offline.test.RequesterStub import RequesterErrorStub

# Create your tests here.
class Importd(unittest.TestCase):

    LOGIN_COOKIES = 'login cookies'

    LOGIN_RESPONSE = MockedResponse('data', LOGIN_COOKIES)

    DECODED_LOGIN_DATA = '''{
        "username": "online user name"
    }'''

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        viewcore.DATABASES = []
        configuration_provider.set_configuration('PARTNERNAME', 'Maureen')
        configuration_provider.set_configuration('DATABASES', 'Sebastian')
        request_handler.stub_me()

    def test_padProtocoll_withNoProtocoll_shouldAddHTPPS(self):
        self.set_up()
        assert import_data._add_protokoll_if_needed('myurl') == 'https://myurl'

    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = import_data.index(GetRequest())
        print(context)
        assert 'ID' in context

    def test_padProtocoll_withExistingProtocoll_shouldNotChangeProtocoll(self):
        self.set_up()
        assert import_data._add_protokoll_if_needed('http://myurl') == 'http://myurl'
        assert import_data._add_protokoll_if_needed('https://myurl') == 'https://myurl'


    def test_init_shouldReturnIndexPage(self):
        self.set_up()
        context = import_data.index(GetRequest())
        assert context['element_titel'] == 'Export / Import'

    _IMPORT_DATA = '''
    #######MaschinenimportStart
    Datum,Kategorie,Name,Wert,Dynamisch
    2017-03-06,Essen,Edeka,-10.0,True
    #######MaschinenimportEnd
    '''

    def test_addePassendeKategorie_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA}))
        assert context['element_titel'] == 'Export / Import'
        assert einzelbuchungen.select().select_year(2017).sum() == -11.54

    def test_import_withOneBuchung_should_showSuccessSingleMessage(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA}))
        assert context['message_content'] ==  '1 Buchung wurde importiert'

    def test_import_withOneBuchung_should_showSuccessMessage(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA_GEMEINSAM}))
        assert context['message_content'] ==  '2 Buchungen wurden importiert'


    _JSON_IMPORT_DATA_GEMEINSAM = '''
    [
    {"id":"122","datum":"2019-01-01","name":"Testausgabe1","kategorie":"Essen","wert":"-1.3", "user": "unknown", "zielperson": "online user name"},
    {"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Essen","wert":"-0.9", "user": "unknown", "zielperson": "Partner"}
    ]
    '''

    def test_gemeinsam_addePassendeKategorie_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

        context = import_data.handle_request(PostRequest({'import':self._IMPORT_DATA_GEMEINSAM}), gemeinsam=True)
        assert context['element_titel'] == 'Export / Import'

        assert len(database_instance().gemeinsamebuchungen.content) == 2

    def test_import_shouldWriteIntoAbrechnungen(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA}))

        written_abrechnung = None
        for key in file_system.instance()._fs_stub.keys():
            if key.startswith('../Import'):
                written_abrechnung = file_system.instance()._fs_stub[key]

        assert written_abrechnung == self._IMPORT_DATA


    def test_addeUnpassendenKategorie_shouldShowImportMappingPage(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'unbekannt', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA}))
        assert context['element_titel'] == 'Kategorien zuweisen'


    def test_addeUnpassendenKategorie_mitPassendemMapping_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Unpassend', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA, 'Essen_mapping':'als Unpassend importieren'}))
        assert context['element_titel'] == 'Export / Import'
        assert einzelbuchungen.select().select_year(2017).sum() == -11.54

    _IMPORT_DATA_GEMEINSAM = '''\n
#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Person,Dynamisch
2019-01-01,Essen,Testausgabe1,-1.3,Sebastian,False
2019-07-11,Essen,Testausgabe2,-0.9,Maureen,False
#######MaschinenimportEnd
'''

    _JSON_IMPORT_DATA = '''
    [
    {"id":"122","datum":"2019-07-15","name":"Testausgabe1","kategorie":"Essen","wert":"-1.3"},
    {"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Essen","wert":"-0.9"}
    ]
    '''

    _JSON_DATA_USERNAME = '''
    {
        "username": "Sebastian",
        "token": "0x00",
        "role": "User"
    }
    '''

    _JSON_DATA_PARTNER = '''
    {
        "partnername": "OnlinePartner"
    }
    '''

    def test_einzelbuchungImport_addePassendeKategorie_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

        requester.INSTANCE = RequesterStub({'https://test.test/einzelbuchung.php': self._JSON_IMPORT_DATA,
                                            'https://test.test/deleteitems.php': '',
                                            'https://test.test/login.php': self._JSON_DATA_USERNAME})

        context = import_data.index(PostRequest({'action': 'load_online_transactions',
                                                 'email': '',
                                                 'server': 'test.test',
                                                 'password': ''}))

        assert context['element_titel'] == 'Export / Import'
        assert len(viewcore.database_instance().einzelbuchungen.content) == 3
        assert viewcore.database_instance().einzelbuchungen.get(1) == {'Datum': datum('11.07.2019'),
            'Dynamisch': False,
            'Kategorie': 'Essen',
            'Name': 'Testausgabe2',
            'Tags': np.nan,
            'Wert': -0.9,
            'index': 1}
        assert viewcore.database_instance().einzelbuchungen.get(2) == {'Datum': datum('15.07.2019'),
            'Dynamisch': False,
            'Kategorie': 'Essen',
            'Name': 'Testausgabe1',
            'Tags': np.nan,
            'Wert': -1.3,
            'index': 2}



        assert requester.instance().call_count_of('https://test.test/deleteitems.php') == 1
        assert requester.instance().complete_call_count() == 2


    def test_gemeinsamImport_addePassendeKategorie_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

        requester.INSTANCE = RequesterStub({'https://test.test/gemeinsamebuchung.php': self._JSON_IMPORT_DATA_GEMEINSAM,
                                           'https://test.test/deletegemeinsam.php' : '',
                                           'https://test.test/login.php': self.LOGIN_RESPONSE},
                                           self.DECODED_LOGIN_DATA,
                                           auth_cookies=self.LOGIN_COOKIES)

        context = import_data.index(PostRequest({'action': 'load_online_gemeinsame_transactions',
                                                      'email': '',
                                                      'server': 'test.test',
                                                      'password' : ''}))

        assert context['element_titel'] == 'Export / Import'
        assert len(database_instance().gemeinsamebuchungen.content) == 2
        assert database_instance().gemeinsamebuchungen.get(0)['Name'] == 'Testausgabe1'
        assert database_instance().gemeinsamebuchungen.get(0)['Person'] == 'Sebastian'
        assert database_instance().gemeinsamebuchungen.get(1)['Name'] == 'Testausgabe2'

        assert requester.instance().call_count_of('https://test.test/deletegemeinsam.php') == 1
        assert requester.instance().complete_call_count() == 3

    _JSON_IMPORT_DATA_GEMEINSAM_WRONG_PARTNER = '''
    [
    {"id":"122","datum":"2019-07-15","name":"Testausgabe1","kategorie":"Essen","wert":"-1.3", "user":"SebastianFalsch","zielperson":"PartnerFalsch"},
    {"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Essen","wert":"-0.9", "user":"SebastianFalsch","zielperson":"online user name"}
    ]
    '''

    def test_gemeinsamImport_withUnpassendenPartnername_shouldImportValueAndRepalceName(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)



        requester.INSTANCE = RequesterStub({'https://test.test/gemeinsamebuchung.php': self._JSON_IMPORT_DATA_GEMEINSAM_WRONG_PARTNER,
                                           'https://test.test/deletegemeinsam.php': '',
                                           'https://test.test/login.php': self.LOGIN_RESPONSE},
                                           self.DECODED_LOGIN_DATA,
                                           auth_cookies=self.LOGIN_COOKIES)

        context = import_data.index(PostRequest({'action': 'load_online_gemeinsame_transactions',
                                                 'email': '',
                                                 'server': 'test.test',
                                                 'password': ''}))

        assert context['element_titel'] == 'Export / Import'
        assert len(viewcore.database_instance().gemeinsamebuchungen.content) == 2
        assert viewcore.database_instance().gemeinsamebuchungen.get(0) == {
            'Datum': datetime.date(2019, 7, 11),
            'Dynamisch': False,
            'Kategorie': 'Essen',
            'Name': 'Testausgabe2',
            'Person': 'Sebastian',
            'Wert': -0.9,
            'index': 0}

        assert viewcore.database_instance().gemeinsamebuchungen.get(1) == {
            'Datum': datetime.date(2019, 7, 15),
            'Dynamisch': False,
            'Kategorie': 'Essen',
            'Name': 'Testausgabe1',
            'Person': 'Maureen',
            'Wert': -1.3,
            'index': 1}

        assert requester.instance().call_count_of('https://test.test/deletegemeinsam.php') == 1
        assert requester.instance().complete_call_count() == 3

    def test_import_withError_shouldShowMessage(self):
        self.set_up()
        requester.INSTANCE = RequesterErrorStub()

        context = import_data.index(PostRequest({'action': 'load_online_gemeinsame_transactions',
                                                      'email': '',
                                                      'server': 'test.test',
                                                      'password' : ''}))

        assert context['message'] == True
        assert context['message_type'] == 'error'
        assert context['message_content'] == 'Verbindung zum Server konnte nicht aufgebaut werden.'


    def test_gemeinsamImport_withUnpassendenKategorie_shouldImportValueAndRequestmapping(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'KeinEssen', 'some name', -1.54)



        requester.INSTANCE = RequesterStub({'https://test.test/gemeinsamebuchung.php': self._JSON_IMPORT_DATA_GEMEINSAM,
                                           'https://test.test/deletegemeinsam.php': '',
                                           'https://test.test/login.php': self.LOGIN_RESPONSE},
                                           self.DECODED_LOGIN_DATA,
                                           auth_cookies=self.LOGIN_COOKIES)

        context = import_data.index(PostRequest({'action': 'load_online_gemeinsame_transactions',
                                                      'email': '',
                                                      'server': 'test.test',
                                                      'password' : ''}))

        assert context['element_titel'] == 'Kategorien zuweisen'
        assert context['import'] == self._IMPORT_DATA_GEMEINSAM
        assert context['unpassende_kategorien'] == ['Essen']


        context = import_data.index(PostRequest({'action': 'map_and_push',
                                                      'Essen_mapping': 'neue Kategorie anlegen',
                                                      'import': self._IMPORT_DATA_GEMEINSAM}))


        assert context['element_titel'] == 'Export / Import'
        assert len(viewcore.database_instance().gemeinsamebuchungen.content) == 2
        assert viewcore.database_instance().gemeinsamebuchungen.content.Person[0] == 'Sebastian'
        assert viewcore.database_instance().gemeinsamebuchungen.content.Person[1] == 'Maureen'

        assert viewcore.database_instance().gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
        assert viewcore.database_instance().gemeinsamebuchungen.content.Kategorie[1] == 'Essen'

        assert requester.instance().call_count_of('https://test.test/deletegemeinsam.php') == 1
        assert requester.instance().complete_call_count() == 3


    def test_set_kategorien_with_ausgeschlossene_kategoerien_should_hide_ausgeschlossene_kategorien(self):
        self.set_up()

        viewcore.database_instance().einzelbuchungen.add(datum('20.01.1990'), 'JaEins', 'SomeTitle', -10)
        viewcore.database_instance().einzelbuchungen.add(datum('20.01.1990'), 'NeinEins', 'SomeTitle', -10)
        viewcore.database_instance().einzelbuchungen.add(datum('20.01.1990'), 'JaZwei', 'SomeTitle', -10)

        configuration.index(PostRequest({'action':'set_ausgeschlossene_kategorien', 'ausgeschlossene_kategorien':'NeinEins'}))

        requester.INSTANCE = RequesterStub({'https://test.test/setkategorien.php': ''})

        import_data.index(PostRequest({'action': 'set_kategorien',
                                              'email': '',
                                              'server': 'test.test',
                                              'password' : ''}))

        assert requester.instance().data_of_request('https://test.test/setkategorien.php')[0]['kategorien'] == 'JaEins,JaZwei'


    def test_upload_data(self):
        self.set_up()

        viewcore.database_instance().gemeinsamebuchungen.add(datum('1.1.2020'), 'kategorie1', 'name1', 1.11, 'Sebastian')
        viewcore.database_instance().gemeinsamebuchungen.add(datum('2.2.2020'), 'kategorie2', 'name2', 2.22, 'Maureen')

        requester.INSTANCE = RequesterStub({'https://test.test/api/gemeinsamebuchung.php': '{"result": "OK"}',
                                            'https://test.test/api/partner.php': self._JSON_DATA_PARTNER,
                                           'https://test.test/api/login.php': self.LOGIN_RESPONSE},
                                           self.DECODED_LOGIN_DATA,
                                           auth_cookies=self.LOGIN_COOKIES
                                           )

        result = import_data.index(PostRequest({'action': 'upload_gemeinsame_transactions',
                                              'email': '',
                                              'server': 'test.test/api',
                                              'password' : ''}))

        assert len(viewcore.database_instance().gemeinsamebuchungen.content) == 0
        assert result['message']
        assert result['message_type'] == 'success'
        assert result['message_content'] == '2 Buchungen wurden erfolgreich hochgeladen.'

        assert requester.INSTANCE.data_of_request('https://test.test/api/gemeinsamebuchung.php') == [
             [
                {
                    'datum': '2020-01-01',
                    'kategorie': 'kategorie1',
                    'name': 'name1',
                    'zielperson': 'online user name',
                    'wert': 1.11
                }
                ,
                {
                    'datum': '2020-02-02',
                    'kategorie': 'kategorie2',
                    'name': 'name2',
                    'zielperson': 'OnlinePartner',
                    'wert': 2.22
                }
            ]
        ]

    def test_upload_data_fehler(self):
        self.set_up()

        viewcore.database_instance().gemeinsamebuchungen.add(datum('1.1.2020'), 'kategorie1', 'name1', 1.11, 'Sebastian')
        viewcore.database_instance().gemeinsamebuchungen.add(datum('2.2.2020'), 'kategorie2', 'name2', 2.22, 'Maureen')

        requester.INSTANCE = RequesterStub({'https://test.test/api/gemeinsamebuchung.php': '{"result": "error"}',
                                            'https://test.test/api/partner.php': self._JSON_DATA_PARTNER,
                                            'https://test.test/api/login.php': self.LOGIN_RESPONSE},
                                           self.DECODED_LOGIN_DATA,
                                           auth_cookies=self.LOGIN_COOKIES)

        result = import_data.index(PostRequest({'action': 'upload_gemeinsame_transactions',
                                              'email': '',
                                              'server': 'test.test/api',
                                              'password' : ''}))

        assert len(viewcore.database_instance().gemeinsamebuchungen.content) == 2
        assert result['message'] == True
        assert result['message_type'] == 'error'
        assert result['message_content'] == 'Fehler beim Hochladen der gemeinsamen Buchungen.'

        assert requester.INSTANCE.data_of_request('https://test.test/api/gemeinsamebuchung.php') == [
             [
                {
                    'datum': '2020-01-01',
                    'kategorie': 'kategorie1',
                    'name': 'name1',
                    'zielperson': 'online user name',
                    'wert': 1.11
                }
                ,
                {
                    'datum': '2020-02-02',
                    'kategorie': 'kategorie2',
                    'name': 'name2',
                    'zielperson': 'OnlinePartner',
                    'wert': 2.22
                }
            ]
        ]

