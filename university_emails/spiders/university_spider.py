import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class EmailItem(Item):
    email = Field()

class UniversitySpider(CrawlSpider):
    name = 'university_spider'
    allowed_domains = ['hu-berlin.de']  
    start_urls = ['https://www.hu-berlin.de/en']  

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(UniversitySpider, self).__init__(*args, **kwargs)
        self.visited_emails = set()  # Set to store visited emails

    def parse_item(self, response):
        loader = ItemLoader(item=EmailItem(), response=response)
        loader.default_output_processor = TakeFirst()

        # Extract emails from various elements 
        emails = response.xpath('//text()').re(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}')

        for email in emails:
            cleaned_email = email.strip().lower()  
            if cleaned_email not in self.visited_emails:
                self.visited_emails.add(cleaned_email)
                loader.add_value('email', cleaned_email)
                yield loader.load_item()