from scrapy import Spider
from scrapy.http import Request, FormRequest
from scrapy.utils.response import open_in_browser

# logging in with scrapy is too much of a hassle but here's an attempt
class LoginSpider(Spider):
    name = 'login'
    def start_requests(self):
        start_url = 'https://www.linkedin.com/login'
        return [Request(url=start_url, callback=self.parse)]

    def parse(self,response):
        print('foo')
        #Get dynamically generated CSRF token
        csrf_token = response.xpath('//*[@name="csrfToken"]/@value').extract_first()
        print('CSRF TOKEN: ', csrf_token)
        return FormRequest.from_response(response,
                                         formdata={'csrfToken': csrf_token, 'password': '', 'username': ''}, callback=self.scrape_pages)
    def scrape_pages(self, response):
        print('response: ', response)
        open_in_browser(response)
