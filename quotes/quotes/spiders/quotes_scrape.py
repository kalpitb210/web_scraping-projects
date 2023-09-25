import scrapy
from pymongo import MongoClient

client = MongoClient("mongodb+srv://kalpit_210:kalpit123@cluster0.y0wtdss.mongodb.net/")

db = client["quotes"]


def scrapy_to_mongo(quote, author, tags):
    collection = db.quotes

    doc = {
        "Quote": quote,
        "Author": author,
        "Tags": tags
    }

    inserted = collection.insert_one(doc)
    return inserted


class QuotesScrapeSpider(scrapy.Spider):
    name = "quotes_scrape"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        container = response.css(".quote")

        for box in container:
            quote = box.css(".text::text").get()
            print(quote)

            author = box.css(".author::text").get()
            print(author)

            tags = box.css(".tags>a::text").getall()
            print(tags)

            print()
            print()

            go_to_mongo = scrapy_to_mongo(quote, author, tags)

        next_page = response.css("li.next>a::attr(href)").get()

        if next_page is not None:
            print(next_page)
            yield response.follow(next_page, callback=self.parse)
