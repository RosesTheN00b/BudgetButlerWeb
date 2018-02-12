import pytest
from selenium import webdriver
import os
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time

class SeleniumTestClass:

    def _to_param(self, name, provider):
        return pytest.param(provider, id=name)

    def pytest_generate_tests(self, metafunc):
        if 'TRAVIS_INTEGRATION' in os.environ:
            chrome_options = Options()
            chrome_options.add_argument("--headless")

            drivers = [self._to_param('Chromium  headless',lambda: _launch_headles_chromium(chrome_options))]
        else:
            drivers = [self._to_param('Chromium', webdriver.Chrome)]

        metafunc.parametrize(argnames='driver_provider', argvalues=drivers, scope="module")

def _launch_headles_chromium(chrome_options):
    if 'TRAVIS_INTEGRATION' in os.environ:
        time.sleep(2) # Sleep 1 sec to avoid mem problems on travis
    return webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options)

def enter_test_mode(driver):
    driver.get('http://localhost:8000/production/testmode')


def fill_element(driver, elementname, content):
    elem = driver.find_element_by_name(elementname)
    elem.clear()
    elem.send_keys(content)

def define_kategorie(driver, kategorie_name):
    driver.get('http://127.0.0.1:8000/configuration/')
    fill_element(driver, 'neue_kategorie', kategorie_name)
    button = driver.find_element_by_id('add_kategorie')
    button.click()

def select_option(driver, option_id, item):
    el = driver.find_element_by_id(option_id)
    for option in el.find_elements_by_tag_name('option'):
        if option.text == item:
            option.click()  # select() in earlier versions of webdriver
            break

def get_options(driver, option_id):
    el = driver.find_element_by_id(option_id)
    result = []
    for option in el.find_elements_by_tag_name('option'):
        result.append(option.text)
    return result

def get_selected_option(driver, option_id):
    select = Select(driver.find_element_by_id(option_id))
    selected_option = select.first_selected_option
    return selected_option.text




