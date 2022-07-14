import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select  # selection of list
from selenium.webdriver.chrome.options import Options  # Options for full screen
import time
from lxml import html
from scrapy.loader import ItemLoader
from marketparser.items import MarketparserItem

class ChromeSpider(scrapy.Spider):
    name = 'chrome'
    allowed_domains = ['chrome.google.com']
    start_urls = ['https://chrome.google.com/webstore/category/extensions']

    def parse(self, response:HtmlResponse):

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

        chrome_options = Options()
        chrome_options.add_argument("start-maximized")

        driver = webdriver.Chrome(executable_path='./chromedriver.exe',
                                  options=chrome_options)  # need to download driver and put in the same directory

        driver.get('https://chrome.google.com/webstore/category/extensions')
        time.sleep(1)


        while True:
            html_source = driver.page_source
            dom = html.fromstring(html_source)
            final_links = set(dom.xpath("//a[@class='a-u']/@href"))


            thumbs = WebDriverWait(driver, 10).until(  # Прогружаем превьюхи
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//a[@class='a-u']"))
            )
            actions = ActionChains(driver)
            actions.move_to_element(thumbs[-1]).perform()
            time.sleep(0.5)
            for l in final_links:
                yield response.follow(l, callback=self.link_parse)

    def link_parse(self, response:HtmlResponse):
        loader = ItemLoader(item=MarketparserItem(), response=response)
        loader.add_value('link', response.url)
        yield loader.load_item()


