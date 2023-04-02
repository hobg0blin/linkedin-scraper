from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import scrapy
import time
import pickle
from dotenv import load_dotenv, find_dotenv #this feels wrong but it works and i don't want two env files
import os

load_dotenv(find_dotenv())
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
#Log in with selenium //
class Selenium():
    def __init__(self):
        chromeOptions = Options()
#        options.add_argument("user-data-dir=C:\\")
#        chromeOptions.headless = True
        self.driver = webdriver.Chrome("/home/brent/scrapism/linkedinscraper/chromedriver", options=chromeOptions)
#        self.login()

    def login(self):
        self.driver.get('http://www.linkedin.com')
        cookies = None
        if (os.path.isfile('./cookies.pickle')):
            cookies = self.load_cookies('./cookies.pickle')
        print('cookies: ', cookies)
        if (cookies != None and len(cookies) > 0):
            print('logged in')
        else:
            self.driver.get('http://www.linkedin.com/login')
        #    time.sleep(5)
            self.driver.find_element(By.ID, "username").send_keys(EMAIL)
            self.driver.find_element(By.ID, "password").send_keys(PASSWORD)
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            self.save_cookies('./cookies.pickle')
        time.sleep(5)

    def get_page_source(self):
        #this should go in feed spider to start requests but need to figure out middleware first
        body = self.driver.page_source
#        return scrapy.http.HtmlResponse(self.driver.current_url, body=body, encoding='utf-8')
        return body

    def quit(self):
        self.driver.quit()

    def save_cookies(self, path):
        with open(path, 'wb') as cookiefile:
            pickle.dump(self.driver.get_cookies(), cookiefile)

    def load_cookies(self, path):
        with open(path, 'rb') as cookiefile:
            cookies = pickle.load(cookiefile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            return cookies


