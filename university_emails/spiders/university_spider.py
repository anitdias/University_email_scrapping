import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
import os
import re

class ContactItem(Item):
    email = Field()
    phone = Field()
    contact_form_link = Field()

class UniversitySpider(CrawlSpider):
    name = 'university_spider'

    def __init__(self, *args, **kwargs):
        super(UniversitySpider, self).__init__(*args, **kwargs)
        self.visited_emails = set()  # Set to store visited emails
        self.visited_phones = set()  # Set to store visited phone numbers
        self.visited_contact_forms = set()  # Set to store visited contact forms

        start_urls_file = kwargs.get('start_urls_file', 'start_urls.txt')
        if os.path.exists(start_urls_file):
            with open(start_urls_file, 'r') as f:
                self.start_urls = [line.strip() for line in f.readlines()]
        else:
            self.start_urls = []
        
        self.allowed_domains = [url.split('/')[2] for url in self.start_urls]

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        loader = ItemLoader(item=ContactItem(), response=response)
        loader.default_output_processor = TakeFirst()

        
        emails = response.xpath('//text()').re(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}')
        for email in emails:
            cleaned_email = email.strip().lower()
            if cleaned_email not in self.visited_emails:
                self.visited_emails.add(cleaned_email)
                loader.add_value('email', cleaned_email)
        
        
        phone_pattern = re.compile(r'''
            (?:\+49\s?[1-9][0-9]{1,4}\s?[0-9]{1,10})   # +49 XXXXXX
            |(?:0[1-9][0-9]{1,4}\s?[0-9]{1,10})        # 0XXXXXX
            |(?:\(?\+49\)?\s?[1-9][0-9]{1,4}[ \-]?[0-9]{1,10}) # +49 (XXXX) XXXXX
            |(?:0[1-9][0-9]{1,4}[ \-]?[0-9]{1,10})     # 0XXX XXXX
            |(?:\d{2,5}[ \-]?\d{3,9})                  # XXXX XXXXX
        ''', re.VERBOSE)
        phones = response.xpath('//text()').re(phone_pattern)
        for phone in phones:
            cleaned_phone = phone.strip()
            
            if cleaned_phone not in self.visited_phones and not re.match(r'\b\d{4}\b', cleaned_phone) and len(cleaned_phone) >= 7:
                self.visited_phones.add(cleaned_phone)
                loader.add_value('phone', cleaned_phone)

        
        contact_form_links = response.xpath('//a[contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "contact") or contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "form") or contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "support") or contains(translate(@href, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "inquiry")]/@href').getall()
        for link in contact_form_links:
            cleaned_link = response.urljoin(link.strip())
            if cleaned_link not in self.visited_contact_forms:
                self.visited_contact_forms.add(cleaned_link)
                loader.add_value('contact_form_link', cleaned_link)

        yield loader.load_item()
