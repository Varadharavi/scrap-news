from datetime import datetime

import scrapy
import hashlib

class ScrapeEtSpider(scrapy.Spider):
    name = "scrape_et"
    allowed_domains = ["economictimes.indiatimes.com"]
    start_urls = ["https://economictimes.indiatimes.com/news/latest-news"]


    def parse(self, response):
        news_list = response.css('div.main_container')
        for article in news_list.css('ul.data li'):
            title = article.css('li a::attr(title)').get()
            link = article.css('li a::attr(href)').get()
            hashed_value = hashlib.sha256(link.encode()).hexdigest()
            yield {"title": title.replace("\t", "").replace("\n", ""),
                   "link": link,
                   "source": "economic_times",
                   "hash": hashed_value,
                   "datetime": datetime.now()}
