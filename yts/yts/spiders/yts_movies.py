import scrapy
from pymongo import MongoClient

client = MongoClient("mongodb+srv://kalpit_210:kalpit123@cluster0.y0wtdss.mongodb.net/")

db = client["yts"]


def mongoos(movie_name, year, genres, keywords, description, director, cast, poster):
    collection = db.yts_movies_data

    doc = {
        "Movie": movie_name,
        "Year": year,
        "Genres": genres,
        "Director": director,
        "Cast": cast,
        "Tags": keywords,
        "Synopsis": description,
        "Movie_Poster": poster
    }

    inserted = collection.insert_one(doc)
    return inserted


class YtsMoviesSpider(scrapy.Spider):
    name = "yts-movies"
    allowed_domains = ["yts.autos"]
    start_urls = ["http://yts.autos/"]

    def data(self, response):
        details = response.css("#movie-info")

        movie_name = details.css("h1::text").get()
        print(movie_name)

        year_genres = details.css("h2::text").getall()

        year = year_genres[0].strip()
        print(year)

        genres = year_genres[1]
        print(genres)

        keywords = response.css("span>a.keyword::text").getall()
        if keywords == []:
            keywords = None
        else:
            keywords = keywords

        print(keywords)

        additional = response.css("#movie-sub-info")
        desc = additional.css("#synopsis>p::text").get()

        if desc is not None:
            description = desc.strip()
        else:
            description = None

        print(description)

        director_box1 = response.css(".directors")
        director_box2 = director_box1.css(".list-cast")
        director = director_box2.css(".list-cast-info>a>span>span::text").get()
        print(director)

        actor_box1 = response.css(".actors")
        cast = actor_box1.css(".list-cast-info>a>span>span::text").getall()
        print(cast)

        poster = response.css("#movie-poster>img::attr(src)").get()
        print(poster)

        go_to_mongo = mongoos(movie_name, year, genres, keywords, description, director, cast, poster)

    def parse(self, response):
        movies = response.css(".browse-movie-wrap>a::attr(href)").getall()

        for movie in movies:
            print(movie)

            yield scrapy.Request(movie, callback=self.data)
