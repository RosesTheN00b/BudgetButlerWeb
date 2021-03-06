import unittest

from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.test.RequestStubs import VersionedPostRequest
from butler_offline.views.sparen import add_order
from butler_offline.core import file_system
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc


class AddOrderTest(unittest.TestCase):
    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        persisted_state.database_instance().sparkontos.add('demokonto', Kontos.TYP_DEPOT)
        persisted_state.database_instance().depotwerte.add('demowert', 'demoisin')
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        context = add_order.index(GetRequest())
        assert context['approve_title'] == 'Order hinzufügen'
        assert context['kontos'] == ['demokonto']
        assert context['depotwerte'] == [{'description': 'demowert (demoisin)', 'isin': 'demoisin'}]
        assert context['typen'] == [add_order.TYP_KAUF, add_order.TYP_VERKAUF]

    def test_init_empty_should_return_error(self):
        self.set_up()
        persisted_state.DATABASE_INSTANCE = None

        context = add_order.index(GetRequest())

        assert '%Errortext' in context
        assert context['%Errortext'] == 'Bitte erfassen Sie zuerst ein Sparkonto vom Typ "Depot".'

    def test_init_without_depotwert_should_return_error(self):
        self.set_up()
        persisted_state.DATABASE_INSTANCE = None
        sparkontos = persisted_state.database_instance().sparkontos
        sparkontos.add('1name', sparkontos.TYP_DEPOT)

        context = add_order.index(GetRequest())

        assert '%Errortext' in context
        assert context['%Errortext'] == 'Bitte erfassen Sie zuerst ein Depotwert.'


    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = add_order.index(GetRequest())
        assert 'ID' in context

    def test_add(self):
        self.set_up()
        add_order.index(VersionedPostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': add_order.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
         ))

        db = persisted_state.database_instance()
        assert len(db.order.content) == 1
        assert db.order.content.Datum[0] == datum('1.1.2017')
        assert db.order.content.Wert[0] == float('2.00')
        assert db.order.content.Name[0] == 'testname'
        assert db.order.content.Depotwert[0] == 'demoisin'
        assert db.order.content.Konto[0] == 'demokonto'

    def test_add_order_should_show_in_recently_added(self):
        self.set_up()
        result = add_order.index(VersionedPostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': add_order.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
         ))
        result_element = list(result['letzte_erfassung'])[0]

        assert result_element['fa'] == 'plus'
        assert result_element['datum'] == '01.01.2017'
        assert result_element['konto'] == 'demokonto'
        assert result_element['name'] == 'testname'
        assert result_element['wert'] == '2,00'
        assert result_element['typ'] == add_order.TYP_KAUF
        assert result_element['depotwert'] == 'demoisin'


    def test_add_should_only_fire_once(self):
        self.set_up()
        next_id = request_handler.current_key()
        add_order.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'datum': rfc('1.1.2017'),
             'name':'testname',
             'wert':'2,00',
             'typ': add_order.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
         ))
        add_order.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'datum': rfc('2.2.2012'),
             'name': 'overwritten',
             'wert': '0,00',
             'typ': add_order.TYP_KAUF,
             'depotwert': 'overwritten',
             'konto': 'overwritten'
             }
         ))
        db = persisted_state.database_instance()
        assert len(db.order.content) == 1
        assert db.order.content.Datum[0] == datum('1.1.2017')
        assert db.order.content.Wert[0] == float('2.00')
        assert db.order.content.Name[0] == 'testname'
        assert db.order.content.Depotwert[0] == 'demoisin'
        assert db.order.content.Konto[0] == 'demokonto'

    def test_edit(self):
        self.set_up()
        add_order.index(VersionedPostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': add_order.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
         ))

        result = add_order.index(VersionedPostRequest(
            {'action': 'add',
             'edit_index': 0,
             'datum': rfc('2.1.2017'),
             'name': '2testname',
             'wert': '3,00',
             'typ': add_order.TYP_VERKAUF,
             'depotwert': '2demoisin',
             'konto': '2demokonto'
             }
         ))

        db = persisted_state.database_instance()
        assert len(db.order.content) == 1
        assert db.order.content.Datum[0] == datum('2.1.2017')
        assert db.order.content.Wert[0] == float('-3.00')
        assert db.order.content.Name[0] == '2testname'
        assert db.order.content.Depotwert[0] == '2demoisin'
        assert db.order.content.Konto[0] == '2demokonto'

        result_element = list(result['letzte_erfassung'])[0]

        assert result_element['fa'] == 'pencil'
        assert result_element['datum'] == '02.01.2017'
        assert result_element['konto'] == '2demokonto'
        assert result_element['name'] == '2testname'
        assert result_element['depotwert'] == '2demoisin'
        assert result_element['wert'] == '3,00'
        assert result_element['typ'] == add_order.TYP_VERKAUF


    def test_edit_should_only_fire_once(self):
        self.set_up()
        add_order.index(VersionedPostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': add_order.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
        ))

        next_id = request_handler.current_key()
        add_order.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'edit_index': 0,
             'datum': rfc('2.1.2017'),
             'name': '2testname',
             'wert': '3,00',
             'typ': add_order.TYP_VERKAUF,
             'depotwert': '2demoisin',
             'konto': '2demokonto'
             }
        ))

        add_order.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'edit_index': 0,
             'datum': rfc('1.1.2010'),
             'name': 'overwritten',
             'wert': '0,00',
             'typ': add_order.TYP_KAUF,
             'depotwert': 'overwritten',
             'konto': 'overwritten'
             }
        ))

        db = persisted_state.database_instance()
        assert len(db.order.content) == 1
        assert db.order.content.Datum[0] == datum('2.1.2017')
        assert db.order.content.Wert[0] == float('-3.00')
        assert db.order.content.Name[0] == '2testname'
        assert db.order.content.Depotwert[0] == '2demoisin'
        assert db.order.content.Konto[0] == '2demokonto'

    def test_editCallFromUeberischt_shouldPresetValues_andRenameButton(self):
        self.set_up()
        add_order.index(VersionedPostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': add_order.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
        ))

        context = add_order.index(PostRequest({'action': 'edit', 'edit_index': '0'}))
        assert context['approve_title'] == 'Order aktualisieren'
        preset = context['default_item']

        assert preset['edit_index'] == '0'
        assert preset['datum'] == '2017-01-01'
        assert preset['konto'] == 'demokonto'
        assert preset['name'] == 'testname'
        assert preset['wert'] == '2,00'
        assert preset['typ'] == add_order.TYP_KAUF
        assert preset['depotwert'] == 'demoisin'

    def test_editCallFromUeberischt_shouldPresetValues_verkauf(self):
        self.set_up()
        add_order.index(VersionedPostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': add_order.TYP_VERKAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
        ))

        context = add_order.index(PostRequest({'action': 'edit', 'edit_index': '0'}))
        assert context['approve_title'] == 'Order aktualisieren'
        preset = context['default_item']

        assert preset['wert'] == '2,00'
        assert preset['typ'] == add_order.TYP_VERKAUF


if __name__ == '__main__':
    unittest.main()
