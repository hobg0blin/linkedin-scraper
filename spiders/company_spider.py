import scrapy
import itertools
from scraper.spiders.selenium_login import Selenium
from scraper.spiders.profile_spider import ProfileSpider
Selector = scrapy.Selector
from w3lib.html import remove_tags
import time
import re

class CompanySpider(ProfileSpider):
    name = "company_spider"
#    selenium = Selenium()
#    selenium.login()
    company_urls = ["https://www.linkedin.com/company/facebook/"]

    def start_requests(self):
        yield scrapy.Request(url="http://google.com", callback=self.parse)

    def parse(self, response):
        pages = map(self.get_company, self.company_urls)
        #print('pages: ', pages)
        # why is map such a nightmare in python
        # is this not pythonic
        # need to research appropriate uses of this
        people = [self.get_people(p) for p in pages]
        for p in people:
            contacts = [self.get_contact(u) for u in p]
            # time.sleep(10)
            foo = self.parse_info(contacts)

            return foo


    def get_company(self, url):
        self.selenium.driver.get(url + 'people')
        time.sleep(10)
        source = self.selenium.get_page_source()
#        self.selenium.driver.quit()
        return source

    def get_people(self, page):
        sel = Selector(text=page)

        urls = sel.xpath("//div[contains(@class, 'org-people-profile-card__profile-info')]//a[contains(@class, 'link-without-visited-state')]/@href").getall()
        proper_urls = [self.add_linkedin(u) for u in urls]
        print('proper urls: ', proper_urls)
        return proper_urls

    def add_linkedin(self, url):
        return 'https://linkedin.com' + url




