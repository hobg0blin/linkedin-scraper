import scrapy
from scraper.spiders.selenium_login import Selenium
Selector = scrapy.Selector
from w3lib.html import remove_tags
import time
import re

class ProfileSpider(scrapy.Spider):
    name = "profile_spider"

    def __init__(self):
        #probably should try to understand the 'super' keyword better
        super(ProfileSpider, self).__init__()
        self.selenium = Selenium()
        self.selenium.login()
        self.linkedin_urls = ['https://linkedin.com/in/garyvaynerchuk/']
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

    def parse_info(self, contact_info):
        for c in contact_info:
            sel = Selector(text=c)
            #TODO: figure out pulling multiple attrs, i.e. get email and personal website or something
            #selector still not working
            #to just get email add:  and contains(@href, 'mailto:')
            links = sel.xpath("//a[contains(@class, 'pv-contact-info__contact-link')]/@href").getall()

            print('links: ', links)
            yield {
                "links":links
            }

    def parse(self, response):
        print('current url', self.selenium.driver.current_url)
        contact_info = map(self.get_contact, self.linkedin_urls)
        return self.parse_info(contact_info)
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
    #TODO move this and parse_info/refactor so that there's no self conflict when company scraper uses them
    def get_contact(self, url):
        print('url: ', url)
        self.selenium.driver.get(url + 'detail/contact-info')
        time.sleep(10)
        data = self.selenium.get_page_source()
#        self.selenium.quit()
        return data





