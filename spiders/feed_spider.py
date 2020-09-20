import scrapy
from scraper.spiders.selenium_login import Selenium
Selector = scrapy.Selector
from w3lib.html import remove_tags
import time
import re

class FeedSpider(scrapy.Spider):
    name = "feed_spider"
    selenium = Selenium()
    #making selenium a class might be dumb bc of stuff like this.
    selenium.login()
    selenium.driver.execute_script("window.scrollTo(0, 10000)")
    time.sleep(10)
    actual_response = selenium.get_page_source()
    selenium.quit()
    def start_requests(self):
        #dummy request to start scrapy TODO: is this necessary? could probably use scrapy middlewares
        yield scrapy.Request(url="http://google.com", callback=self.parse)

    def parse(self, response):

        #since we're not actually using the response object, we can't use its built-in selector - we have to declare one
#        print(self.actual_response.body)
#        print('response: ', self.actual_response)
#        print('get body tag', Selector(response=self.actual_response).xpath('//body'))
        sel = Selector(text=self.actual_response)
#        print('body tag: ', sel.xpath("//body"));
        for text in sel.xpath("//div[contains(@class, 'feed-shared-text')]//span[@dir='ltr']").getall():
            if not text.encode('utf-16', 'surrogatepass').isspace():
                output = remove_tags(text)
                yield {
                    "text": output
                }

