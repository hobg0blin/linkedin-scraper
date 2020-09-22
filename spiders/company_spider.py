import scrapy
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
        print('company urls', self.company_urls)
        pages = map(self.get_company, self.company_urls)
        #print('pages: ', pages)
        people = map(self.get_people, pages)
        print('people: ', list(people))
        for p in people:
            print('p: ', p)
            for q in p:
                print('q: ', q)

            print('get contact: ', self.get_contact)
            contacts = list(map(self.get_contact, p))
            print('contacts: ', contacts)
            # time.sleep(10)
            self.parse_info(contacts)


    def get_company(self, url):
        self.selenium.driver.get(url + 'people')
        time.sleep(10)
        source = self.selenium.get_page_source()
        print('source: ', source)
#        self.selenium.driver.quit()
        return source

    def get_people(self, page):
        sel = Selector(text=page)

        urls = sel.xpath("//div[contains(@class, 'org-people-profile-card__profile-info')]//a[contains(@class, 'link-without-visited-state')]/@href").getall()
        print('urls: ', urls)
        return map(self.add_linkedin, urls)

    def add_linkedin(self, url):
        return 'https://linkedin.com' + url




