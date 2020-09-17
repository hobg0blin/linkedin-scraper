from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import scrapy
from scrapy import Selector
import time
from dotenv import load_dotenv
import os

load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

#Log in with selenium // TODO: make Selenium a class, add any necessary utility functions

class Selenium():
    def __init__(self):
        chromeOptions = Options()
        chromeOptions.headless = True
        self.driver = webdriver.Chrome(options=chromeOptions)

    def login(self):
        self.driver.get('http://www.linkedin.com/login')
    #    time.sleep(5)
        self.driver.find_element_by_id("username").send_keys(EMAIL)
        self.driver.find_element_by_id("password").send_keys(PASSWORD)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()

    def get_page_source(self):
        #this should go in feed spider to start requests but need to figure out middleware first
        body = self.driver.page_source
#        return scrapy.http.HtmlResponse(self.driver.current_url, body=body, encoding='utf-8')
        return body

    def quit(self):
        self.driver.quit()

class FeedSpider(scrapy.Spider):
    name = "feed_spider"
    driver = Selenium()
    driver.login()
    actual_response = driver.get_page_source()
    driver.quit()
    def start_requests(self):
        #dummy request to start scrapy TODO: is this necessary? could probably use scrapy middlewares
        yield scrapy.Request(url="http://google.com", callback=self.parse)

    def parse(self, response):

        #since we're not actually using the response object, we can't use its built-in selector - we have to declare one
#        print(self.actual_response.body)
        print('response: ', self.actual_response)
#        print('get body tag', Selector(response=self.actual_response).xpath('//body'))
        sel = Selector(text=self.actual_response)
        print('body tag: ', sel.xpath("//body"));
        for text in sel.xpath("//div[contains(@class, 'feed-shared-text')]/span[@dir='ltr']/text()").getall():
            print('text:', text)
            yield {
                'text': text
            }

