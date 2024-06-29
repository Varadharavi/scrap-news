from datetime import datetime

import scrapy
import hashlib

class McScraperSpider(scrapy.Spider):
    name = "scrape_mc"
    allowed_domains = ["moneycontrol.com"]
    start_urls = ["https://moneycontrol.com"]


    def parse(self, response):
        news_list = response.css('#keynwstb2 ul.tabs_nwsconlist')
        for article in news_list.css('li'):
            title = article.css('li a::text').get()
            link = article.css('li a::attr(href)').get()
            hashed_value = hashlib.sha256(link.encode()).hexdigest()
            yield {"title": title.replace("\t", "").replace("\n", ""),
                   "link": link,
                   "source": "moneycontrol",
                   "hash": hashed_value,
                   "datetime": datetime.now()}