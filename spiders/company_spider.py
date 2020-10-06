import scrapy
import itertools
from scraper.spiders.selenium_login import Selenium
from scraper.spiders.profile_spider import ProfileSpider
from scraper.items import ImageItem
Selector = scrapy.Selector
from w3lib.html import remove_tags
import time
import re

class CompanySpider(ProfileSpider):
    name = "company_spider"
#    selenium = Selenium()
#    selenium.login()j
    company_urls = ["https://www.linkedin.com/company/facebook/"]

    def start_requests(self):
        yield scrapy.Request(url="http://google.com", callback=self.parse)

    def parse(self, response):
        pages = self.get_company_from_search(self.company_urls)
        #print('pages: ', pages)
        # why is map such a nightmare in python
        # is this not pythonic
        # need to research appropriate uses of this
        people = itertools.chain.from_iterable(self.get_people_from_search(pages))
        print('people: ', people)
        #have to force processing of 'people' generator with a list() function here, otherwise pages after the first iteration aren't actually loaded before we try to process them
        #at least i think that's what's happening
        #list() fixed it anyway
        #FIXME selenium is double-loading pages for some reason
        #contact_pages = [self.get_contact_page(p) for p in list(people)]
        #return self.get_contact(contact_pages)
        profiles = self.get_main_profiles(list(people))
        pictures = self.get_profile_picture(profiles)
        print('pictures: ', pictures)
        yield ImageItem(image_urls = pictures)
#        for p in people:
#            print('p: ', p)
#            yield {
#                "person": p
#            }
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
            time.sleep(5)

            #TODO: could probably combine this with click_see_more in ProfileSpider for a utility function, have it live in SeleniumLogin?
            # old version, doesn't loook like this attribute is there anymore?
        #  see_employees = self.selenium.driver.find_element_by_xpath('//a[@data-control-name="topcard_see_all_employees"]')
            see_employees = self.selenium.driver.find_element_by_xpath('//div[contains(@class, "mt2") and not(contains(@class, "org-top-card-secondary-content__connections"))]//a[contains(@href, "/search/results/people")]')
            self.selenium.driver.execute_script("arguments[0].click()", see_employees)
            time.sleep(10)
            pages = 0
            while pages < 5:
                time.sleep(2)
                i = 100;
                while i < 3000:
                    self.selenium.driver.execute_script("window.scrollTo(0,{});".format(i))
                    # time.sleep(1)
                    i += 200
                time.sleep(3)
                print('current url: ', self.selenium.driver.current_url)
                next_button = self.selenium.driver.find_element_by_xpath('//button[contains(@class, "artdeco-pagination__button--next")]')
                self.selenium.driver.execute_script("arguments[0].click()", next_button)

                page = (self.selenium.get_page_source())
                print('url in while loop: ', self.selenium.driver.current_url)
                pages += 1
                yield page

    def get_people_from_search(self, pages):
        url_count = 0
        for p in pages:
            sel = Selector(text=p)
            urls = sel.xpath("//div[contains(@class, 'search-result--person')]//div[contains(@class, 'search-result__info')]//a[contains(@class, 'search-result__result-link ')]/@href").getall()
            proper_urls = [self.add_linkedin(u) for u in urls]
            print('proper_urls', proper_urls)
            url_count += len(proper_urls)
            print('url count: ', url_count)
            yield proper_urls


    def get_people_from_company_page(self, page):
        sel = Selector(text=page)

        urls = sel.xpath("//div[contains(@class, 'org-people-profile-card__profile-info')]//a[contains(@class, 'link-without-visited-state')]/@href").getall()
        proper_urls = [self.add_linkedin(u) for u in urls]
        print('proper urls: ', proper_urls)
        return proper_urls

    def add_linkedin(self, url):
        return 'https://linkedin.com' + url




