import scrapy
import itertools
from linkedinscraper.spiders.selenium_login import Selenium
from linkedinscraper.spiders.profile_spider import ProfileSpider
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from linkedinscraper.items import ImageItem
Selector = scrapy.Selector
from w3lib.html import remove_tags
import random
import time
import re
failed_pages = []
page_start = 10
page_end = 60

class CompanySpider(ProfileSpider):
    name = "company"
    selenium = Selenium()
    selenium.login()
    company_urls = ["https://www.linkedin.com/search/results/all/?keywords=meta&origin=GLOBAL_SEARCH_HEADER&sid=h_-"]

    def start_requests(self):
        yield scrapy.Request(url="http://google.com", callback=self.parse)

    def parse(self, response):
        pages = self.get_company_from_search(self.company_urls)
        # why is map such a nightmare in python
        # is this not pythonic
        # need to research appropriate uses of this
        people = itertools.chain.from_iterable(self.get_people_from_search(pages))
        #have to force processing of 'people' generator with a list() function here, otherwise pages after the first iteration aren't actually loaded before we try to process them
        #at least i think that's what's happening
        #list() fixed it anyway
        #FIXME selenium is double-loading pages for some reason
        #contact_pages = [self.get_contact_page(p) for p in list(people)]
        #return self.get_contact(contact_pages)
        #ughhh listing it in print consumes it because its a damn iterable
        # NOTE TO SELF NEVER FUCKING CONSUME THE DAMN ITERABLE WHY IS PYTHON LIKE THIS
        # this should just get you a bunch of links, which you can then run the Profile spider on - you can also use the code below to run both in one, but I've been getting locked out when I do this.
        people_list = list(people)
        yield people_list
#        print("people: ", people_list)
#        profiles = self.get_main_profiles(people_list)
#        prof_list = list(profiles)
#        details = self.get_info(prof_list)
#        pictures = self.get_profile_picture(prof_list)
#        pic_list = list(pictures)
#        for idx, p in enumerate(list(details)):
#            yield {
#                "person": p,
#                "image_urls": [pic_list[idx]],
#                "images": [pic_list[idx]]
#            }
        self.selenium.quit()

#        for p in people:
            # GET BIO
        #for p in people:
        #    profiles = self.get_main_profiles(p)
        #    #FIXME: should probably have a uniform rule about where for loops are allowed ot live - profile and bio functions should be same
        #    bios = self.get_bios(profiles)
        #    return bios
        #GET CONTACT INFO
        # contacts = [self.get_contact_page(u) for u in p]
        # time.sleep(10)
        # foo = self.get_contact(contacts)

#            return bios


    def get_company(self, url):
        self.selenium.driver.get(url + 'people')
        time.sleep(10)
        source = self.selenium.get_page_source()
#        self.selenium.driver.quit()
        return source

    def get_company_from_search(self, urls):
        for url in urls:
            self.selenium.driver.get(url)
            time.sleep(random.randint(1, 5))

            #TODO: could probably combine this with click_see_more in ProfileSpider for a utility function, have it live in SeleniumLogin?
            # old version, doesn't loook like this attribute is there anymore?
        #  see_employees = self.selenium.driver.find_element_by_xpath('//a[@data-control-name="topcard_see_all_employees"]')
            see_employees = self.selenium.driver.find_element(By.XPATH, '//div[@id="search-reusables__filters-bar"]//button[contains(., "People")]')
            self.selenium.driver.execute_script("arguments[0].click()", see_employees)
            pages = page_start
            # go to desired page
            if page_start > 0:
                self.selenium.driver.get('https://www.linkedin.com/search/results/people/?keywords=meta&origin=SWITCH_SEARCH_VERTICAL&page=' + str(page_start) + '&sid=PcB')
            time.sleep(5)
            while pages < page_end:
                print("starting page: ", pages)
                time.sleep(random.randint(1, 2) * 0.25)
                i = 200;
                while i < 2000:
                    self.selenium.driver.execute_script("window.scrollTo(0,{});".format(i))
                    time.sleep(random.randint(1, 3) * 0.01)
                    i += random.randint(100, 300)
                wait = WebDriverWait(self.selenium.driver, 3000000000);
                wait.until(EC.visibility_of_element_located((By.XPATH, '//button[contains(@class, "artdeco-pagination__button--next")]')))
                next_button = self.selenium.driver.find_element(By.XPATH, '//button[contains(@class, "artdeco-pagination__button--next")]')
                page = (self.selenium.get_page_source())
                print("finished page: ", pages)
                try:
                    self.selenium.driver.execute_script("arguments[0].click()", next_button)
                    pages += 1
                except NoSuchElementException:
                    print("failed finding next button on page ", pages)
                    break
                yield page

    def get_people_from_search(self, pages):
        url_count = 0
        for p in pages:
            sel = Selector(text=p)
            urls = sel.xpath("//div[contains(@class, 'entity-result__item')]//span[contains(@class, 'entity-result__title-text')]//a[contains(@class, 'app-aware-link')]/@href").getall()
            # proper_urls = [self.add_linkedin(u) for u in urls]
            url_count += len(urls)
            yield urls


    def get_people_from_company_page(self, page):
        sel = Selector(text=page)

        urls = sel.xpath("//div[contains(@class, 'org-people-profile-card__profile-info')]//a[contains(@class, 'link-without-visited-state')]/@href").getall()
        proper_urls = [self.add_linkedin(u) for u in urls]
        return proper_urls

    def add_linkedin(self, url):
        return 'https://linkedin.com' + url




