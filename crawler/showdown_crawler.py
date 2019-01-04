from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
import time

ban_list = set(['Mewtwo', 'Mew', 'Lugia', 'Ho-Oh', 'Celebi', 'Kyogre', 'Groudon', 'Rayquaza', 'Jirachi', 'Deoxys', 'Dialga', 'Palkia', 'Giratina',
            'Phione', 'Manaphy', 'Darkrai', 'Shaymin', 'Arceus', 'Victini', 'Reshiram', 'Zekrom', 'Kyurem', 'Kyurem-Black', 'Keldeo', 'Meloetta', 'Genesect',
            'Xerneas', 'Yveltal', 'Zygarde', 'Diancie', 'Hoopa', 'Hoopa-Unbounded' 'Volcanion', 'Cosmog', 'Cosmoem', 'Solgaleo', 'Lunala', 'Necrozma', 'Magearna', 'Marshadow'])
chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome('/home/jw/Documents/chromedriver', chrome_options=chrome_options)
browser.set_page_load_timeout(300)
browser.set_script_timeout(300)
#browser.get('http://replay.pokemonshowdown.com/search/?format=gen7ou&rating')
browser.get('http://replay.pokemonshowdown.com/search/?format=gen7ou')
WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.NAME, 'moreResults')))
for i in range(0, 24):
    browser.find_elements_by_name('moreResults')[0].click()
    time.sleep(3)
    print(i)
links = browser.find_elements_by_xpath('//a[contains(@href, "/gen7ou-")]')
print(len(links))
with open('showdown3.csv', 'w') as output:
    for link in links:
        url = link.get_attribute('href')+'.log'
        browser.execute_script('window.open("' + url + '", "new_window")')
        browser.switch_to_window(browser.window_handles[1])
        time.sleep(1)
        log_file = browser.find_element_by_tag_name('pre').get_attribute('innerHTML').split('\n')
        if (log_file[-3].find('rating') == -1) or (log_file[-2].find('rating') == -1):
            browser.switch_to_window(browser.window_handles[0])
            continue
        p1 = log_file[-3].find('rating');
        p2 = log_file[-2].find('rating')
        print(log_file[-3])
        print(log_file[-2])
        rating1 = int(log_file[-3][p1+8:p1+12])
        rating2 = int(log_file[-2][p2+8:p2+12])
        print(rating1)
        print(rating2)
        if (rating1 < 1300) and (rating2 < 1300):
            browser.switch_to_window(browser.window_handles[0])
            continue
        n1 = 0
        n2 = 0
        n = 0
        team1 = []
        team2 = []
        for line in log_file:
            if line.find('|poke|p1|') != -1:
                n += 1
                print(line)
                pokemon = line.split('|')[3].split(',')[0]
                if pokemon not in ban_list:
                    team1.append(pokemon)
                    n1 += 1
            if line.find('|poke|p2|') != -1:
                n += 1
                print(line)
                pokemon = line.split('|')[3].split(',')[0]
                if pokemon not in ban_list:
                    team2.append(pokemon)
                    n2 += 1
            if n == 12:
                print(n1)
                print(n2)
                break
        if n1 == 6:
            output.write(','.join(team1) + '\n')
        if n2 == 6:
            output.write(','.join(team2) + '\n')
        browser.switch_to_window(browser.window_handles[0])
