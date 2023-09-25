import scrapy
from pymongo import MongoClient

client = MongoClient("mongodb+srv://kalpit_210:kalpit123@cluster0.y0wtdss.mongodb.net/")

db = client["anime"]


def to_database(name, poster, age_rating, video_quality, total_episodes, length, final_desc):
    collection = db.anime_data

    docs = {
        "Name": name,
        "Poster": poster,
        "Rated": age_rating,
        "Quality": video_quality,
        "Episodes": total_episodes,
        "Length": length,
        "Description": final_desc
    }

    inserted = collection.insert_one(docs)
    return inserted


class AnimeDataSpider(scrapy.Spider):
    name = "anime_data"
    allowed_domains = ["aniwatch.to"]
    start_urls = ["https://aniwatch.to/az-list"]

    def anime_detailss(self, response):
        name = response.css(".anisc-detail>h2::text").get()
        print(name)

        poster = response.css(".film-poster>img::attr(src)").get()
        print(poster)

        more_details = response.css(".tick")
        age_rating = more_details.css(".tick-pg::text").get()
        print(age_rating)

        video_quality = more_details.css(".tick-quality::text").get()
        print(video_quality)

        total_episodes = more_details.css(".tick-eps::text").get()
        print(total_episodes)

        episode_length = more_details.css(".item::text").getall()
        length = episode_length[1]
        print(length)

        description = response.css(".film-description>div.text::text").get()
        final_desc = description.strip()
        print(final_desc)

        print()
        print()

        go_to_mongo = to_database(name, poster, age_rating, video_quality, total_episodes, length, final_desc)
        print(go_to_mongo)

    def parse(self, response):
        a = response.css(".tab-content")
        b = a.css(".block_area-content")
        c = b.css(".film_list-wrap")

        for d in c:
            e = d.css(".flw-item")

            links = e.css(".film-poster>a")

            for link in links:
                url = f"https://aniwatch.to/{link.attrib['href']}"

                yield scrapy.Request(url, callback=self.anime_detailss)
