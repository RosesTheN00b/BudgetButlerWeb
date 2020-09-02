import unittest
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore import viewcore
from butler_offline.core.database import Database

class NonPersistedStateTest(unittest.TestCase):
    
    def clear_context(self):
        non_persisted_state.CONTEXT = {}
        viewcore.DATABASE_INSTANCE = Database('db')


    def test_einzelbuchungen(self):
        self.clear_context()

        assert non_persisted_state.get_changed_einzelbuchungen() == []

        non_persisted_state.add_changed_einzelbuchungen('demo')

        assert non_persisted_state.get_changed_einzelbuchungen() == ['demo']


    def test_dauerauftraege(self):
        self.clear_context()

        assert non_persisted_state.get_changed_dauerauftraege() == []

        non_persisted_state.add_changed_dauerauftraege('demo')

        assert non_persisted_state.get_changed_dauerauftraege() == ['demo']


    def test_gemeinsame_buchungen(self):
        self.clear_context()

        assert non_persisted_state.get_changed_gemeinsamebuchungen() == []

        non_persisted_state.add_changed_gemeinsamebuchungen('demo')

        assert non_persisted_state.get_changed_gemeinsamebuchungen() == ['demo']


if __name__ == '__main__':
    unittest.main()
