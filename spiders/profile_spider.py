import scrapy
from scraper.spiders.selenium_login import Selenium
Selector = scrapy.Selector
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
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
       # self.selenium.quit()
        return data

    #again, need to figure out middlewares so this dummy req isn't here
    def start_requests(self):
        yield scrapy.Request(url="http://google.com", callback=self.parse)

    def get_contact(self, contact_info):
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
        #contact_info = map(self.get_contact_page, self.linkedin_urls)
        #return self.get_contact(contact_info)
        profiles = self.get_main_profiles(self.linkedin_urls)
        return self.get_bios(profiles)

    def get_main_profiles(self, urls):
       for u in urls:
        print('getting profile: ', u)
        self.selenium.driver.get(u)
        time.sleep(5)
        self.click_see_more()
        time.sleep(1)
        data = self.selenium.get_page_source()
        yield data

    def click_see_more(self):
        try:
            show_more = self.selenium.driver.find_element(By.ID, "line-clamp-show-more-button")
        except NoSuchElementException:
            print("no show more button")
            return
        self.selenium.driver.execute_script("arguments[0].click();", show_more);
        time.sleep(1)
        #nice little recursion in the event that it's a super long bio
        self.click_see_more()


    def get_bios(self, pages):
        for p in pages:
            sel = Selector(text=p)
            bio = sel.xpath("//p[contains(@class, 'pv-about__summary-text')]").get()
            if bio is not None:
                clean_bio = re.sub('see more$', '', remove_tags(bio))
                yield {
                    "bio": clean_bio
                }


    def get_posts(self):
        profile_data = map(self.get_profile_data, self.linkedin_urls)
        for d in profile_data:
            sel = Selector(text=d)
            print('body tag: ', sel.xpath("//body"));
            for text in sel.xpath("//div[contains(@class, 'feed-shared-text')]//span[@dir='ltr']").getall():
                if not text.encode('utf-16', 'surrogatepass').isspace():
                    output = remove_tags(text)
                    yield {
                        "text": output
                    }
    #TODO move this and parse_info/refactor so that there's no self conflict when company scraper uses them
    def get_contact_page(self, url):
        print('url: ', url)
        self.selenium.driver.get(url + 'detail/contact-info')
        time.sleep(1)
        data = self.selenium.get_page_source()
#        self.selenium.quit()
        return data





