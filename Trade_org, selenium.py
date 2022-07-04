#Selenium / Authorization / Dynamic website.

# The task was to collect trading information between certain list of countries. Trade.org is dynamically
# generated web site and direct links to necessary tables didn't work that's why Selenium was used from the
# very beginning of parsing including authorization.




from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
from pprint import pprint
from lxml import html
import requests

client = MongoClient('127.0.0.1', 27017)
db = client['Export']
export = db.export_import



header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

chrome_options = Options()
chrome_options.add_argument("start-maximized")

s = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.get('https://www.trademap.org/Index.aspx')

button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_MenuControl_marmenu_login')))
button.click()

login = driver.find_element(By.ID, 'Username')
login.send_keys('')

passw = driver.find_element(By.ID, 'Password')
passw.send_keys('')

passw.send_keys(Keys.ENTER)

button = driver.find_element(By.ID, 'ctl00_PageContent_label_RadioButton_TradeType_Export')
button.click()

product_code = driver.find_element(By.ID, 'ctl00_PageContent_RadComboBox_Product_Input')
product_code.click()
product_code.send_keys('310230')

button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'ctl00_PageContent_RadComboBox_Product_c0'))
)
button.click()

country_from = driver.find_element(By.ID, 'ctl00_PageContent_RadComboBox_Country_Input')
country_from.click()
country_from.send_keys('br')

button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'ctl00_PageContent_RadComboBox_Country_c0'))
)
button.click()

button = driver.find_element(By.ID, 'ctl00_PageContent_RadioButtonList_Partner_1')
button.click()

country_to = driver.find_element(By.ID, 'ctl00_PageContent_RadComboBox_Partner_Input')
country_to.click()
country_to.send_keys('Latin')

button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'ctl00_PageContent_RadComboBox_Partner_c0'))
)
button.click()

button = driver.find_element(By.ID, 'ctl00_PageContent_Button_TimeSeries')
button.click()

time.sleep(2)

selection = driver.find_element(By.ID, 'ctl00_NavigationControl_DropDownList_OutputOption')
select = Select(selection)
select.select_by_value('ByCountry')



selection = driver.find_element(By.ID, 'ctl00_NavigationControl_DropDownList_Partner_Group')
select = Select(selection)
select.select_by_value('-2') #partner none

time.sleep(1)

selection = driver.find_element(By.ID, 'ctl00_PageContent_GridViewPanelControl_DropDownList_NumTimePeriod')
select = Select(selection)
select.select_by_value('5')

selection = driver.find_element(By.ID, 'ctl00_PageContent_GridViewPanelControl_DropDownList_PageSize')
select = Select(selection)
select.select_by_value('100')



html_source = driver.page_source
dom = html.fromstring(html_source)
table = dom.xpath("//table[@id='ctl00_PageContent_MyGridView1']")


export_data_2 = []
lines = table[0].xpath("//tr[@align='right']")

for l in lines:
    export_data = {}
    country_ = l[1].text_content()
    year2017 = l[2].text_content()
    year2018 = l[3].text_content()
    year2019 = l[4].text_content()
    year2020 = l[5].text_content()
    year2021 = l[6].text_content()

    export_data['country_to'] = country_
    export_data['country_from'] = 'Brazil'
    export_data['2017'] = year2017
    export_data['2018'] = year2018
    export_data['2019'] = year2019
    export_data['2020'] = year2020
    export_data['2021'] = year2021
    export_data['type'] = 'export'
    export_data['values'] = 'USD'

    export_data_2.append(export_data)

selection = driver.find_element(By.ID, 'ctl00_NavigationControl_DropDownList_TS_Indicator')
select = Select(selection)
select.select_by_value('Q')

html_source = driver.page_source
dom = html.fromstring(html_source)
table = dom.xpath("//table[@id='ctl00_PageContent_MyGridView1']")
lines = table[0].xpath("//tr[@align='right']")


for l in lines:
    export_data = {}
    country_ = l[1].text_content()
    year2017 = l[2].text_content()
    year2018 = l[3].text_content()
    year2019 = l[4].text_content()
    year2020 = l[5].text_content()
    year2021 = l[6].text_content()

    export_data['country_to'] = country_
    export_data['country_from'] = 'Brazil'
    export_data['2017'] = year2017
    export_data['2018'] = year2018
    export_data['2019'] = year2019
    export_data['2020'] = year2020
    export_data['2021'] = year2021
    export_data['type'] = 'export'
    export_data['values'] = 'TONS'

    export_data_2.append(export_data)










# _______________________________________
List = ['Pe', 'Co', 'Me', 'Ch', 'Ar', 'Pa', 'Co', 'Ho', 'Ec', 'Gu', 'Ni', 'Do', 'Su', 'Gu', 'Ur', 'Cu', 'El']
List2 = ['Peru', 'Colombia', 'Mexico', 'Chile', 'Argentina', 'Panama', 'Costa Rica', 'Honduras', 'Ecuador', 'Guatemala',
         'Nicaragua', 'Dominican Republic', 'Suriname', 'Guyana', 'Uruguay', 'Cuba', 'El Salvador']

i = 0

for el in List:

    country = driver.find_element(By.ID, 'ctl00_NavigationControl_DropDownList_Country')
    selection = Select(country)

    selection.select_by_visible_text(List2[i])

    selection = driver.find_element(By.ID, 'ctl00_NavigationControl_DropDownList_TS_Indicator')
    select = Select(selection)
    select.select_by_value('V')

    html_source = driver.page_source
    dom = html.fromstring(html_source)
    table = dom.xpath("//table[@id='ctl00_PageContent_MyGridView1']")




    lines = table[0].xpath("//tr[@align='right']")

    for l in lines:
        export_data = {}
        country_ = l[1].text_content()
        year2017 = l[2].text_content()
        year2018 = l[3].text_content()
        year2019 = l[4].text_content()
        year2020 = l[5].text_content()
        year2021 = l[6].text_content()

        export_data['country_to'] = country_
        export_data['country_from'] = List2[i]
        export_data['2017'] = year2017
        export_data['2018'] = year2018
        export_data['2019'] = year2019
        export_data['2020'] = year2020
        export_data['2021'] = year2021
        export_data['type'] = 'export'
        export_data['values'] = 'USD'

        export_data_2.append(export_data)


    selection = driver.find_element(By.ID, 'ctl00_NavigationControl_DropDownList_TS_Indicator')
    select = Select(selection)
    select.select_by_value('Q')

    html_source = driver.page_source
    dom = html.fromstring(html_source)
    table = dom.xpath("//table[@id='ctl00_PageContent_MyGridView1']")
    lines = table[0].xpath("//tr[@align='right']")

    for l in lines:
        export_data = {}
        country_ = l[1].text_content()
        year2017 = l[2].text_content()
        year2018 = l[3].text_content()
        year2019 = l[4].text_content()
        year2020 = l[5].text_content()
        year2021 = l[6].text_content()

        export_data['country_to'] = country_
        export_data['country_from'] = List2[i]
        export_data['2017'] = year2017
        export_data['2018'] = year2018
        export_data['2019'] = year2019
        export_data['2020'] = year2020
        export_data['2021'] = year2021
        export_data['type'] = 'export'
        export_data['values'] = 'TONS'

        export_data_2.append(export_data)

    i += 1


export.insert_many(export_data_2)


