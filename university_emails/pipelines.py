# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import csv

class UniversityEmailsPipeline:
    def process_item(self, item, spider):
        return item

import csv

class CsvWriterPipeline:
    def open_spider(self, spider):
        self.file = open('emails.csv', 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['email'])  
        self.emails_seen = set()  

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        email = item.get('email')
        if email and email not in self.emails_seen:
            self.emails_seen.add(email)
            self.writer.writerow([email])
        return item