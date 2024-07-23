# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html



from itemadapter import ItemAdapter
import csv

class UniversityEmailsPipeline:
    def process_item(self, item, spider):
        return item

class CsvWriterPipeline:
    def open_spider(self, spider):
        
        self.email_file = open('emails.csv', 'w', newline='')
        self.phone_file = open('phones.csv', 'w', newline='')
        self.contact_form_file = open('contact_forms.csv', 'w', newline='')

        
        self.email_writer = csv.writer(self.email_file)
        self.phone_writer = csv.writer(self.phone_file)
        self.contact_form_writer = csv.writer(self.contact_form_file)

       
        self.email_writer.writerow(['email'])
        self.phone_writer.writerow(['phone'])
        self.contact_form_writer.writerow(['contact_form_link'])

       
        self.emails_seen = set()
        self.phones_seen = set()
        self.contact_forms_seen = set()

    def close_spider(self, spider):
        
        self.email_file.close()
        self.phone_file.close()
        self.contact_form_file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        email = adapter.get('email')
        phone = adapter.get('phone')
        contact_form_link = adapter.get('contact_form_link')
        
        if email and email not in self.emails_seen:
            self.emails_seen.add(email)
            self.email_writer.writerow([email])

        if phone and phone not in self.phones_seen:
            self.phones_seen.add(phone)
            self.phone_writer.writerow([phone])

        if contact_form_link and contact_form_link not in self.contact_forms_seen:
            self.contact_forms_seen.add(contact_form_link)
            self.contact_form_writer.writerow([contact_form_link])

        return item
