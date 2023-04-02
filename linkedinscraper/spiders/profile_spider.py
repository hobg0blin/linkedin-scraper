import scrapy
from linkedinscraper.spiders.selenium_login import Selenium
Selector = scrapy.Selector
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from w3lib.html import remove_tags
from linkedinscraper.items import ImageItem
import random
import json
import time
import re
import os

class ProfileSpider(scrapy.Spider):
    name = "profile"

    def __init__(self):
        #probably should try to understand the 'super' keyword better
        super(ProfileSpider, self).__init__()
        print('cwd: ', os.getcwd())
        # status_file = open('./last_run_stats.json')
        # status = json.load(status_file)
        # status = {"end_index": 0}
        ## TODO: create blank status file if none is present
        #print('status file: ', status)
        status = {"completed_urls": [], "end_index": 0}

        self.completed_urls = status["completed_urls"]
        self.start = status["end_index"]
        self.end = status["end_index"] + 20
        #status_file.close()
        #GET URLS AND OPEN THEM HERE
        url_file = open('./google_first_50_pages.json')
        data = json.load(url_file)
        self.linkedin_urls = data['items']['urls']
        print('url count, total: ', len(self.linkedin_urls))
        print('url count, remaining: ', len(self.linkedin_urls) - self.start)
        if (self.end >len(self.linkedin_urls)):
            self.end = len(self.linkedin_urls) - 1
        self.linkedin_urls = self.linkedin_urls[self.start:self.end]

        self.selenium = Selenium()
        self.selenium.login()
#        self.linkedin_urls = ['https://linkedin.com/in/garyvaynerchuk/']
            # this is where we should pass args to determine which part of the profile to scrape, but just testing with posts for now
    #what was this doing again? recent activity?
    def get_profile_data(self, url):
        self.selenium.driver.get(url + 'detail/recent-activity/shares')
        time.sleep(random.randint(2, 5))
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
        prof_list = list(profiles)
        #return self.get_bios(profiles)
        pic_urls = self.get_profile_picture(prof_list)
        #TODO figure out how to point bio info to an image link
        profile_data = self.get_info(prof_list)
        details = list(profile_data)
        pics =list(pic_urls)
        with open("last_run_stats.json", "w") as stats:
            json.dump({"completed_urls": self.completed_urls, "end_index": self.end}, stats)

        for idx, p in enumerate(list(details)):
            yield {
                "person": p,
                "image_urls": [pics[idx]],
                "images": [pics[idx]]
            }
#        yield ImageItem(image_urls=pic_urls)


    def get_profile_picture(self, pages):
        for p in pages:
            sel = Selector(text=p)
            image = sel.xpath("//img[contains(@class, 'pv-top-card-profile-picture__image')]/@src").get()
            print('got image: ', image)
            yield image


    def get_main_profiles(self, urls):
       print('getting profiles: ', urls)
       for idx, u in enumerate( urls ):
        if u in self.completed_urls:
            print('already did this one! ', u)
            continue
        self.completed_urls.append(u)
        print ('on url #: ', idx)
        print('getting profile: ', u)
        self.selenium.driver.get(u)
        time.sleep(random.randint(1,2))
        wait = WebDriverWait(self.selenium.driver, 3000000000);
        wait.until(lambda x: self.check_exists_by_id("ssIFrame_google"))
        wait_captcha = WebDriverWait(self.selenium.driver, 300000000);
        wait_captcha.until(lambda x: self.check_exists_by_id("captcha-internal"))

        #TODO this should just be a utility function on the selenium class
        i = 100;
        while i < 3000:
            self.selenium.driver.execute_script("window.scrollTo(0,{});".format(i))
            # time.sleep(1)
            i += random.randint(1, 3)* 100
        time.sleep(random.randint(0, 2))
#        print('background is present: ', self.selenium.driver.find_element(By.XPATH, '//div[@id="oc-background-section"]'))

        self.click_see_more()
#        time.sleep(1)
        data = self.selenium.get_page_source()
        if (idx % 10 == 0 and idx != 0 ):
            time.sleep(random.randint(5, 10))
        if  (idx % 50 == 0 and idx != 0):
            time.sleep(random.randint(150, 250))

        #self.end = self.end + 1
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


    def get_info(self, pages):
        for p in pages:
            sel = Selector(text=p)
            bio = sel.xpath("//div[contains(@class, 'ph5') and contains(@class, 'pv3')]//div[contains(@class, 'pv-shared-text-with-see-more')]").get()
            name = sel.xpath("//h1/text()").get()
            title = sel.xpath("//div[contains(@class, 'ph5')]//div[contains(@class, 'pv-text-details__left-panel')]//div[contains(@class, 'text-body-medium')]/text()").get()
            past_jobs = sel.xpath("//div[contains(@class, 'pvs-list__outer-container')]//li[contains(@class, 'pvs-list__item--line-separated')]").getall()
            loc = sel.xpath("//div[contains(@class, 'pv-text-details__left-panel')]//span[contains(@class, 'text-body-small')]/text()").get()
#currently not gettin nothin it's fine i'll fix it later
#            history = []
#            for j in past_jobs:
#                sel = Selector(text=j)
#                past_title = sel.xpath("//span[contains(@class, 'mr1')]/text()").getall()
#                details = sel.xpath("//span[contains(@class, 't-14')]/text()").getall()
#                desc = sel.xpath("div[contains(@class, 'pv-shared-text-with-see-more')]/text()").getall()
#                desc = (' ').join(desc)
#                history.append({
#                    'past_title': past_title,
#                    'details': details,
#                    'location': loc,
#                    'description': desc
#                })
#
            if bio is not None:
                clean_bio = re.sub('see more$', '', remove_tags(bio))
                yield {
                    "bio": clean_bio,
                    "name": name,
                    "title": title,
                    "loc": loc,
#                    "history": history
                }
            else:
                yield {
                    "name": name,
                    "title": title,
                    "loc": loc,
#                    "history": history
                }


    def get_posts(self):
        profile_data = map(self.get_profile_data, self.linkedin_urls)
        for d in profile_data:
            sel = Selector(text=d)
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
    def check_exists_by_id(self, id):
        try:
            self.selenium.driver.find_element(By.ID, id)
        except NoSuchElementException:
            return True
        print('NEED TO LOG IN AGAIN YA DIPSHIT')
        os.system("say 'need to log in again, ya dipshit'")
        return False



