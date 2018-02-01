'''
Created on 23.11.2017

@author: sebastian
'''
from SeleniumTest import SeleniumTestClass
from time import sleep
from SeleniumTest import get_selected_option

class TestHeadlines(SeleniumTestClass):
    def test_add_dauerauftrag(self, driver_provider):
        driver = driver_provider()
        driver.get('http://localhost:8000/adddauerauftrag/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Neuer Dauerauftrag'
        driver.close()

    def test_add_einnahme(self, driver_provider):
        driver = driver_provider()
        driver.get('http://localhost:8000/addeinnahme/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Neue Einnahme'
        driver.close()

    def test_add_einzelbuchung(self, driver_provider):
        driver = driver_provider()
        driver.get('http://localhost:8000/addeinzelbuchung/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Neue Ausgabe'
        driver.close()

    def test_add_gemeinsam(self, driver_provider):
        driver = driver_provider()
        driver.get('http://localhost:8000/addgemeinsam/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Neue gemeinsame Ausgabe'
        driver.close()

    def test_configuration(self, driver_provider):
        driver = driver_provider()
        driver.get('http://localhost:8000/configuration/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Einstellungen'
        driver.close()

    def test_dashboard(self, driver_provider):
        driver = driver_provider()
        driver.get('http://localhost:8000/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Übersicht'
        driver.close()

    def test_dauerauftragsuebersicht(self, driver_provider):
        driver = driver_provider()
        driver.get('http://localhost:8000/dauerauftraguebersicht/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Alle Daueraufträge'
        driver.close()

    def test_gemeinsam_abrechnen(self, driver_provider):
        driver = driver_provider()
        driver.get('http://localhost:8000/gemeinsamabrechnen/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Gemeinsam abrechnen'
        driver.close()

    def test_gemeinsam_uebersicht(self, driver_provider):
        driver = driver_provider()
        driver.get('http://localhost:8000/gemeinsameuebersicht/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Alle gem. Buchungen'
        driver.close()

    def test_importd(self, driver_provider):
        driver = driver_provider()
        driver.get('http://localhost:8000/import/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Datensätze importieren'
        driver.close()

    def test_jahresuebersicht(self, driver_provider):
        driver = driver_provider()
        driver.get('http://localhost:8000/jahresuebersicht/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Jahresübersicht'

    def test_monatsuebersicht(self, driver_provider):
        driver = driver_provider()
        driver.get('http://localhost:8000/monatsuebersicht/')
        assert driver.find_element_by_id('pagetitle').get_attribute('innerHTML') == 'Monatsübersicht'

