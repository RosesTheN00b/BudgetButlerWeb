import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from core.DatabaseModule import Database
from gemeinsamuebersicht import views
import viewcore




# Create your tests here.
class Gemeinsamuebersicht(unittest.TestCase):

    def setUp(self):
        print("create new database")
        self.testdb = Database("test")
        viewcore.viewcore.DATABASE_INSTANCE = self.testdb
        viewcore.viewcore.DATABASES = ['test']
        viewcore.viewcore.TEST = True

    def test_init(self):
        self.setUp()
        result = views.handle_request(GetRequest())


class GetRequest():
    method = "GET"