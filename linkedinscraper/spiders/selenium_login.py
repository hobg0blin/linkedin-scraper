from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import scrapy
import time
from dotenv import load_dotenv, find_dotenv #this feels wrong but it works and i don't want two env files
import os

load_dotenv(find_dotenv())
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
#Log in with selenium //
class Selenium():
    def __init__(self):
        chromeOptions = Options()
#        chromeOptions.headless = True
        self.driver = webdriver.Chrome("/home/brent/scrapism/linkedinscraper/chromedriver", options=chromeOptions)
#        self.login()

    def login(self):
        self.driver.get('http://www.linkedin.com/login')
    #    time.sleep(5)
        self.driver.find_element(By.ID, "username").send_keys(EMAIL)
        self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(15)

    def get_page_source(self):
        #this should go in feed spider to start requests but need to figure out middleware first
        body = self.driver.page_source
#        return scrapy.http.HtmlResponse(self.driver.current_url, body=body, encoding='utf-8')
        return body

    def quit(self):
        self.driver.quit()


