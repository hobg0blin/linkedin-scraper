import scrapy
from scraper.spiders.selenium_login import Selenium
Selector = scrapy.Selector
from w3lib.html import remove_tags
import time
import re

class ProfileSpider(scrapy.Spider):
    name = "profile_spider"
    #is it worth making a parent class that just logs into selenium? e.g. class ProfileSpider extends linkedinlogin or something
    selenium = Selenium()
    selenium.login()
    linkedin_urls = ["https://www.linkedin.com/in/garyvaynerchuk/"]
    # this is where we should pass args to determine which part of the profile to scrape, but just testing with posts for now
    def get_profile_data(self, url):
        self.selenium.driver.get(url + 'detail/recent-activity/shares')
        self.selenium.driver.execute_script("window.scrollTo(0, 10000)")
        time.sleep(10)
        data = self.selenium.get_page_source()
        self.selenium.quit()
        return data

    #again, need to figure out middlewares so this dummy req isn't here
    def start_requests(self):
        yield scrapy.Request(url="http://google.com", callback=self.parse)

    def parse(self, response):
        contact_info = map(self.get_contact, self.linkedin_urls)
        for c in contact_info:
            sel = Selector(text=c)
            #TODO: figure out pulling multiple attrs, i.e. get email and personal website or something
            print('body tag: ', sel.xpath("//body"))
            #selector still not working
            for email in sel.xpath("//a[contains(@class, 'pv-contact-info__contact-link') and contains(@href, 'mailto:')]/text()").getall():
                yield {
                    "email": email
                }
        #working code to get posts from a profile
        #profile_data = map(self.get_profile_data, self.linkedin_urls)
        #for d in profile_data:
        #    sel = Selector(text=d)
        #    print('body tag: ', sel.xpath("//body"));
        #    for text in sel.xpath("//div[contains(@class, 'feed-shared-text')]//span[@dir='ltr']").getall():
        #        if not text.encode('utf-16', 'surrogatepass').isspace():
        #            output = remove_tags(text)
        #            yield {
        #                "text": output
        #            }
    def get_contact(self, url):
        self.selenium.driver.get(url + 'detail/contact-info')
        data = self.selenium.get_page_source()
        self.selenium.quit()
        return data





