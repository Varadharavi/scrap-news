import hashlib
from datetime import datetime

import scrapy


class LivemintScraperSpider(scrapy.Spider):
    name = "livemint_scraper"
    allowed_domains = ["livemint.com"]
    start_urls = ["https://www.livemint.com/latest-news"]

    def parse(self, response):
        for article in response.css('h2.headline'):
            title = article.css('a::text').get()
            link = article.css('a::attr(href)').get()
            hashed_value = hashlib.sha256(link.encode()).hexdigest()
            yield {"title": title.strip(),
                   "link": "https://livemint.com" + link,
                   "source": "livemint",
                   "hash": hashed_value,
                   "datetime": datetime.now()}
