from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import json

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome('/home/jw/Documents/chromedriver', chrome_options=chrome_options)
browser.set_page_load_timeout(300)
browser.set_script_timeout(300)
#browser.get('http://replay.pokemonshowdown.com/search/?format=gen7ou&rating')
browser.get('https://dex.pokemonshowdown.com/pokemon/')
time.sleep(2)
browser.get('https://play.pokemonshowdown.com/data/pokedex.js?fc21ad5d')
text = browser.find_element_by_tag_name('pre').get_attribute('innerHTML')[24:-1]
p = 0
while True:
    p = text.find(':', p+3)
    if p == -1:
        break
    else:
        #print(p)
        i = p-1
        while text[i] != ',' and text[i] != '{':
            i -= 1
        if text[i+1] != '"':
            text = text[0:i+1] + '"' + text[i+1:p] + '"' + text[p:]

dic = json.loads(text)
dic_new = {}
for key, value in dic.items():
    if key == 'meltan':
        break
    if '-Mega' not in value['species']:
        dic_new[value['species']] = {'num':value['num'], 'types':value['types'], 'baseStats':[value['baseStats']['hp'], value['baseStats']['atk'], value['baseStats']['def'], value['baseStats']['spa'], value['baseStats']['spd'], value['baseStats']['spe']]}

with open('pokedex.json', 'w') as output:
    json.dump(dic_new, output)
    
