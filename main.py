import scrapy
import json
import mongo
from pymongo import MongoClient


def mongo_connect_and_insert():
    try:
        CONNECTION_STRING = "mongodb+srv://root:root@cluster0.wscsruq.mongodb.net/test"
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


def writeFile(apartment):
    jsonstring = json.dumps(apartment)
    jsonfile = open('apartment.json', 'w')
    jsonfile.write(jsonstring)
    jsonfile.close()


def urls_brands():
    primary_url = 'https://www.vivareal.com.br/venda/sp/paulinia/apartamento_residencial/?pagina='
    final_url = list()
    for i in range(2, 44 + 1):
        final_url.append(primary_url + str(i))
    return final_url

def writeFiles(apartaments):
    jsonstring = json.dumps(apartaments)
    jsonfile = open('apartaments.json', 'w')
    jsonfile.write(jsonstring)
    jsonfile.close()


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = urls_brands()
    apartment_Data = list()

    def parse(self, response):
        print(self.start_urls)
        for title in response.css('.js-card-selector'):
            name = title.css('.property-card__title::text').get()
            endereco = title.css('.property-card__address::text').get()
            price = title.css('.property-card__values div > p::text').get()
            condo_price = title.css('.js-condo-price::text').get()
            banheiros = title.css('.property-card__details > li:nth-child(2) > span::text').get()
            vagas = title.css('.property-card__details > li:nth-child(3) > span::text').get()

            self.apartment_Data.append(
                {'NOME_IMOVEL': name, 'RUA': endereco, 'PREÇO_IMOVEL': price, 'CONDOMINIO_PREÇO': condo_price,
                 'BANHEIROS': banheiros, 'VAGAS': vagas}, )
            yield {'NOME_IMOVEL': name, 'RUA': endereco, 'PREÇO_IMOVEL': price, 'CONDOMINIO_PREÇO': condo_price,
                   'BANHEIROS': banheiros, 'VAGAS': vagas}

    def close(self, reason):
        urls_brands()
        writeFiles(self.apartment_Data)
        mongo_connect_and_insert()