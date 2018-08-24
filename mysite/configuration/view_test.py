'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from test.FileSystemStub import FileSystemStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from configuration import views
from core import FileSystem
from core.DatabaseModule import Database
from viewcore import viewcore
from viewcore import request_handler
from viewcore import configuration_provider
from viewcore.converter import datum_from_german as datum

class TestKonfiguration(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        configuration_provider.LOADED_CONFIG = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        views.index(GetRequest())

    def test_addKategorie(self):
        self.set_up()
        views.index(PostRequest({'action':'add_kategorie', 'neue_kategorie':'test'}))
        assert viewcore.database_instance().einzelbuchungen.get_alle_kategorien() == set(['test'])

    def test_change_db_should_trigger_db_reload(self):
        self.set_up()
        views.index(PostRequest({'action':'edit_databases', 'dbs':'test'}))
        assert viewcore.database_instance().name == 'test'

        views.index(PostRequest({'action':'edit_databases', 'dbs':'test2'}))
        assert viewcore.database_instance().name == 'test2'

    def test_change_partnername_should_change_partnername(self):
        self.set_up()
        assert viewcore.name_of_partner() == 'kein_Partnername_gesetzt'
        views.index(PostRequest({'action':'set_partnername', 'partnername':'testpartner'}))
        assert viewcore.name_of_partner() == 'testpartner'

    def test_change_themecolor_should_change_partnername(self):
        self.set_up()
        assert configuration_provider.get_configuration('THEME_COLOR') == '#00acd6'
        views.index(PostRequest({'action':'change_themecolor', 'themecolor':'#000000'}))
        assert configuration_provider.get_configuration('THEME_COLOR') == '#000000'

    def test_change_partnername_should_mirgrate_old_partnernames(self):
        self.set_up()
        name_of_partner = viewcore.name_of_partner()
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen
        gemeinsame_buchungen.add(datum('01.01.2017'), 'kat', 'name', 1, name_of_partner)

        views.index(PostRequest({'action':'set_partnername', 'partnername':'testpartner_renamed'}))
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen
        database_partners = gemeinsame_buchungen.content.Person

        assert set(database_partners) == set(['testpartner_renamed'])

    def test_change_colors(self):
        self.set_up()
        assert viewcore.design_colors() == '3c8dbc,f56954,00a65a,00c0ef,f39c12,d2d6de,001F3F,39CCCC,3D9970,01FF70,FF851B,F012BE,8E24AA,D81B60,222222,d2d6de'.split(',')
        views.index(PostRequest({'action': 'change_colorpalette',
                                 '0_checked': 'on',
                                 '0_farbe' : '#000000',
                                 '1_checked': 'on',
                                 '1_farbe': '#FFFFFF',
                                 '2_farbe': '#555555'}))
        assert viewcore.design_colors() == ['000000', 'FFFFFF']
        self.set_up()
