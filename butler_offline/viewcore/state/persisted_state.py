from butler_offline.core import DBManager
from butler_offline.viewcore import configuration_provider
from butler_offline.viewcore.state import persisted_state


DATABASE_INSTANCE = None
DATABASES = []


def database_instance():
    '''
    returns the actual database instance
    '''
    if not persisted_state.DATABASES:
        persisted_state.DATABASES = configuration_provider.get_configuration('DATABASES').split(',')

    if persisted_state.DATABASE_INSTANCE is None:
        ausgeschlossene_kategorien = set(
            configuration_provider.get_configuration('AUSGESCHLOSSENE_KATEGORIEN').split(','))
        persisted_state.DATABASE_INSTANCE = DBManager.read(persisted_state.DATABASES[0],
                                                           ausgeschlossene_kategorien=ausgeschlossene_kategorien)
    return persisted_state.DATABASE_INSTANCE


def switch_database_instance(database_name):
    ausgeschlossene_kategorien = set(configuration_provider.get_configuration('AUSGESCHLOSSENE_KATEGORIEN').split(','))
    persisted_state.DATABASE_INSTANCE = DBManager.read(database_name, ausgeschlossene_kategorien=ausgeschlossene_kategorien)


def _save_database():
    if persisted_state.DATABASE_INSTANCE:
        DBManager.write(persisted_state.DATABASE_INSTANCE)


def _save_refresh():
    _save_database()
    db_name = persisted_state.DATABASE_INSTANCE.name
    persisted_state.DATABASE_INSTANCE = None
    switch_database_instance(db_name)


def save_tainted():
    db = persisted_state.DATABASE_INSTANCE
    if db.is_tainted():
        print('Saving database with', db.taint_number(), 'modifications')
        _save_refresh()
        print('Saved')
