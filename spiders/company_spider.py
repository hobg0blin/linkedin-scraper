import scrapy
from scraper.spiders.selenium_login import Selenium
Selector = scrapy.Selector
from w3lib.html import remove_tags
import time
import re

class CompanySpider(scrapy.Spider):
    name = "company_spider"
    selenium = Selenium()
    selenium.login()
    company_urls = ["https://www.linkedin.com/company/facebook/"]

    def start_requests(self):
        yield scrapy.Request(url="http://google.com", callback=self.parse)

    def parse(self, response):
        pages = map(self.get_company, self.company_urls)
        for i in pages:
            return self.get_people(i)


    def get_company(self, url):
        self.selenium.driver.get(url + 'people')
        time.sleep(10)
        source = self.selenium.get_page_source()
        self.selenium.driver.quit()
        print('source: ', source)
        return source

    def get_people(self, page):
        sel = Selector(text=page)
        print('page: ', page)

        print('body tag: ', sel.xpath("//body"))
        for person in sel.xpath("//div[contains(@class, 'org-people-profile-card__profile-title')]/text()").getall():
            print('person: ', person)
            yield {
                "person": person
            }




