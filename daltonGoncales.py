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
    jsonfile = open('daltonGoncales.json', 'w')
    jsonfile.write(jsonstring)
    jsonfile.close()


def urls_brands():
    primary_url = 'https://www.daltongoncales.com.br/imoveis/para-alugar/casa+sobrado?finalidade=residencial'
    final_url = list()
    for i in range(2, 44 + 1):
        final_url.append(primary_url + str(i))
    return final_url

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://www.daltongoncales.com.br/imoveis/para-alugar/casa+sobrado?finalidade=residencial', 'https://www.daltongoncales.com.br/imoveis/para-alugar/casa+sobrado?finalidade=residencial&pagina=2%27']
    daltongoncales = list()

    def parse(self, response):
        for title in response.css('.link-all'):
            district = title.css('.card-title::text').get()
            place = title.css('.card-text::text').get()
            description = title.css('.description::text').get()
            bedroom = title.css('.value > p > span::text').get()
            bathroom = title.css('.values .value:nth-child(2) > p > span::text').get()
            vacancy = title.css('.values .value:nth-child(3) > p > span::text').get()
            square_meters = title.css('.values .value:nth-child(4) > p > span::text').get()
            self.daltongoncales.append({'DISTRICT': district, 'PLACE': place, 'DESCRIPTION': description, 'BEDROOM': bedroom, 'BATHROOM': bathroom, 'VACANCY': vacancy, 'SQUARE_METERS': square_meters})
            yield {'DISTRICT':district, 'PLACE': place, 'DESCRIPTION': description, 'BEDROOM': bedroom, 'BATHROOM': bathroom, 'VACANCY': vacancy, 'SQUARE_METERS': square_meters}

    def close(self, reason):
        writeFiles(self.daltongoncales)