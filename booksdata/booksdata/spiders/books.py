import scrapy
from pathlib import Path
from pymongo import MongoClient




client = MongoClient("mongodb+srv://kalpit_210:kalpit123@cluster0.y0wtdss.mongodb.net/")

db = client["books"]

def scrapy_to_mongo(filename, title, image_link, rating, price, inStock):
    collection = db[filename]

    doc = {
        "Book Name": title,
        "Image": image_link,
        "Rating": rating,
        "In Stock": inStock,
        "Price": price
    }

    inserted = collection.insert_one(doc)
    return inserted



class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]




    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
            "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html",
            "https://books.toscrape.com/catalogue/category/books/horror_31/index.html",
            "https://books.toscrape.com/catalogue/category/books/food-and-drink_33/index.html",
            "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html",
            "https://books.toscrape.com/catalogue/category/books/romance_8/index.html",
            "https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        book_genre = response.url.split("/")[-2]

        index = 0
        filename = ""
        for char in book_genre:
            if char == "_":
                filename = book_genre[0:index].title().replace("-", " ")
                break
            else:
                index = index+1

        print(filename)


        Path(book_genre).write_bytes(response.body)
        self.log(f"Saved file {book_genre}")

        cards = response.css(".product_pod")

        for card in cards:
            print()
            a = card.css(".image_container>a>img").attrib["src"]
            image = a.replace("../../../../", "https://books.toscrape.com/")
            print(image)

            book_name = card.css("h3>a::text").get()
            print(book_name)

            rating = card.css(".star-rating").attrib["class"].split(" ")[-1]
            print(rating)

            price = card.css(".product_price>p::text").get()
            print(price)

            c = card.css(".instock")
            if len(c.css(".icon-ok")) > 0:
                inStock = True
            else:
                inStock = False
            print(inStock)

            go_to_mongo = scrapy_to_mongo(filename, book_name, image, rating, price, inStock)
            print(go_to_mongo)



