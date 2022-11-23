import scrapy
import json
import mongo
from pymongo import MongoClient


def mongo_connect_and_insert():
    try:
        CONNECTION_STRING = "mongodb+srv://matheushenry1:123@cluster0.jruob8s.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(CONNECTION_STRING)
        db = client.vivareal
        collection = db.vivareal

        with open('apartaments.json') as file:
            file_data = json.load(file)

        if isinstance(file_data, list):
            collection.insert_many(file_data)
        else:
            collection.insert_one(file_data)

        print('success')
    except:
        print('fail')


def writeFiles(apartment):
    jsonstring = json.dumps(apartment)
    jsonfile = open('casa.json', 'w')
    jsonfile.write(jsonstring)
    jsonfile.close()


def urls_brands():
    primary_url = 'https://www.vivareal.com.br/venda/sp/paulinia/apartamento_residencial/?pagina='
    final_url = list()
    for i in range(2, 44 + 1):
        final_url.append(primary_url + str(i))
    return final_url

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://www.emcasa.com/imoveis/sp/sao-paulo/jardim-paulista/jardim-paulistano/jardins?ad_id=610195689816&gclid=CjwKCAiApvebBhAvEiwAe7mHSMcdkK2R_YkJezpOdZ-5N97g5LHJNOVXIc3KYeeyXJeorYXo3nUEZhoCjusQAvD_BwE&pg=3&utm_campaign=go_src_sp_by_conv_cvs-lsa_dsa&utm_content=610195689816&utm_medium=search&utm_source=google']
    casas = list()

    def parse(self, response):
        for title in response.css('.src-components-listings-Card-__styles-module___ecListingCard'):
            price = title.css('.src-components-listings-Card-__styles-module___ecListingCard__price::text').get()
            adress = title.css('.src-components-listings-Card-__styles-module___ecListingCard__text::text').get()
            description = title.css('div.src-components-listings-Card-__styles-module___ecListingCard__body > p:nth-child(3)::text').get()
            self.casas.append({'PRICE': price, 'ADRESS': adress, 'DESCRIPTION': description})
            yield {'PRICE': price, 'ADRESS':adress, 'DESCRIPTION': description}

    def close(self, reason):
        writeFiles(self.casas)