import sys, os
import unittest
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")
'''
'''
from viewcore import configuration_provider
from core import FileSystem
from test.FileSystemStub import FileSystemStub



class TesteConverter(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        configuration_provider.LOADED_CONFIG = None

    def test_configuration_provider_shouldLoadDefault_ifNoFileProvided(self):
        self.set_up()
        assert configuration_provider.get_configuration('DATABASES') == configuration_provider.DEFAULT_CONFIG['DATABASES']

    def test_configuration_provider_shouldExtendLoadedConfig_ifKeyMissing(self):
        self.set_up()
        configuration_provider.set_configuration('test', 'bla')
        assert configuration_provider.get_configuration('DATABASES') == configuration_provider.DEFAULT_CONFIG['DATABASES']

    def test_configuration_provider_should_load_values(self):
        self.set_up()
        configuration_provider.set_configuration('test', 'bla')
        assert configuration_provider.get_configuration('test') == 'bla'

    def test_configuration_provider_should_save_values(self):
        self.set_up()
        configuration_provider.set_configuration('test','bla')
        assert configuration_provider.get_configuration('test') == 'bla'
        configuration_provider.set_configuration('test','not bla')
        assert configuration_provider.get_configuration('test') == 'not bla'

    
