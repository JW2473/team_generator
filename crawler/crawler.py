from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
import json

chrome_options = Options()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("prefs", prefs)
browser = webdriver.Chrome('/home/jw/Documents/chromedriver', chrome_options=chrome_options)
#browser = webdriver.Chrome('/home/jw/Documents/chromedriver')
browser.set_page_load_timeout(300)
browser.set_script_timeout(300)
browser.get('http://www.pokemon-gl.com/')
WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btnLink')))
elements = browser.find_elements_by_xpath('//a[@class="btnLink"]')
for element in elements:
    if element.get_attribute('innerHTML') == 'English':
        element.click()
        break
WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'headerNavigation')))
elements = browser.find_elements_by_id('cookie-dismisser')
if len(elements) > 0:
    elements[0].click()
browser.find_elements_by_id('headerNavigation')[0].click()
print(browser.current_url)
#browser.find_element_by_id('headerNavigation').click()
browser.find_elements_by_xpath('//a[@href="/rentalteam/"]')[0].click()
print(browser.current_url)
time.sleep(3)
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/rentalteam/usum/"]')))
element.click()
#browser.find_elements_by_xpath('//a[@href="/rentalteam/usum/"]')[0].click()
print(browser.current_url)
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btnCrLarge')))
element.click()
#browser.find_elements_by_css_selector('.btnCrLarge')[0].click()
element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'battleTypeTab')))
print(browser.current_url)
#element.click()
#element = browser.find_elements_by_id('battleTypeTab')[0]
element.find_elements_by_css_selector('.single')[0].click()
time.sleep(1)
browser.find_elements_by_css_selector('.total')[0].click()
WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/rentalteam/usum/BT-")]')))
browser.find_elements_by_css_selector('.search-battleteam')[0].click()
element = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'execSearch')))
element.click()
WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/rentalteam/usum/BT-")]')))
with open('rentalTeams2.csv', 'w') as output:
    last_url = ''
    while(True):
        print(browser.current_url)
        elements = browser.find_elements_by_xpath('//a[contains(@href, "/rentalteam/usum/BT-")]')
        '''
        if last_url == elements[0].get_attribute('href'):
            break;
        else:
            last_url = elements[0].get_attribute('href');
        '''
        browser.execute_script('window.open("' + elements[0].get_attribute('href') + '", "new_window")')
        browser.switch_to_window(browser.window_handles[1])
        browser.switch_to_window(browser.window_handles[0])
        i = 0
        while i < len(elements):
            url = elements[i].get_attribute('href')
            browser.execute_script('window.open("' + url + '", "new_window")')
            browser.switch_to_window(browser.window_handles[1])
            #time.sleep(t)
            while True:
                try:
                    WebDriverWait(browser, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.pokemon')))
                    break
                except TimeoutException:
                    browser.refresh()
            print(browser.current_url)
            pokemons = browser.find_elements_by_css_selector('.pokemon')
            print(len(pokemons))
            s = {}
            s['winCount'] = browser.find_elements_by_css_selector('.btWinCount')[0].get_attribute('innerHTML')
            s['useCount'] = browser.find_elements_by_css_selector('.btUseCount')[0].get_attribute('innerHTML');
            s['pokemons'] = []
            for pokemon in pokemons:
                s['pokemons'].append(pokemon.find_elements_by_css_selector('.name')[0].get_attribute('innerHTML'));
                '''
                elements = pokemon.find_elements_by_css_selector('.types')[0].find_elements_by_xpath('*');
                if len(elements) == 1:
                    p['types'] = (elements[0].get_attribute('innerHTML'), elements[1].get_attribute('innerHTML'))
                else:
                    p['types'] = (elements[0].get_attribute('innerHTML'), elements[0].get_attribute('innerHTML'))
    
                Item = pokemon.find_elements_by_css_selector('.value')[1].get_attribute('innerHTML').split(' ');
                p['mega'] = (Item[0][0:3] == p['name'][0:3]) and (Item[0][-3:-1] == 'ite')
                '''
            output.write(json.dumps(s) + '\n')
            browser.switch_to_window(browser.window_handles[0])
            i += 1

        while True:
            try:
                browser.find_elements_by_css_selector('.btnArrowRight')[0].click()
                output.flush()
                time.sleep(5)
                break
            except WebDriverException:
                print('!')
                browser.find_elements_by_css_selector('.footerBtn')[0].click()
                time.sleep(0.5)
