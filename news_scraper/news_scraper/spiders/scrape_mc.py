from datetime import datetime

import scrapy
import hashlib
from pymongo import MongoClient


class ScrapeMcSpider(scrapy.Spider):
    name = "scrape_mc"
    allowed_domains = ["moneycontrol.com"]
    start_urls = []

    def __init__(self, *args, **kwargs):
        super(ScrapeMcSpider, self).__init__(*args, **kwargs)
        self.mongo_uri = 'mongodb+srv://bearbullfolio:2Yy0qdkolyiW3xbG@bearbullfolio-cluster1.26telbo.mongodb.net/'  # Replace with your MongoDB URI
        self.mongo_db = 'bearbullfolio'  # Replace with your database name

    def start_requests(self):
        # Connect to MongoDB and retrieve URLs
        client = MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        holding_collection = db['current_holdings_list']  # Replace with your collection name
        ticker_collection = db['ticker_list']
        documents = holding_collection.find().distinct("ticker")
        for ticker in documents:
            try:
                ticker_data = ticker_collection.find_one({"symbol": ticker})
                yield scrapy.Request(url=ticker_data['mc_url'], callback=self.parse, meta={"ticker": ticker})
            except KeyError:
                print(f"{ticker} - Keyerror")

    def parse(self, response):
        try:
            ticker = response.meta.get('ticker')
            head_news = response.css('div#news div.clearfix h3')
            heading = head_news.css('a::text').get()
            url = head_news.css('a::attr(href)').get()
            date_string = response.css('div#news div.clearfix div.newsblock1 span::text').get()
            datetime_object = datetime.strptime(date_string, "%b %d %Y %I:%M %p")
            hashed_value = hashlib.sha256(ticker.encode() + url.encode()).hexdigest()
            yield dict(ticker=ticker, hashed_value=hashed_value, heading=heading, url=url, date=datetime_object)

            news_list = response.css('div#news div.clearfix p').extract()
            for url_html in news_list:
                url_selector = scrapy.Selector(text=url_html)
                heading = url_selector.css('a::text').get()
                url = url_selector.css('a::attr(href)').get()
                date_string = url_selector.css('span::text').get()
                if url is not None:
                    hashed_value = hashlib.sha256(ticker.encode() + url.encode()).hexdigest()
                    datetime_object = datetime.strptime(date_string, "%b %d %Y %I:%M %p")
                    yield dict(ticker=ticker, hashed_value=hashed_value, heading=heading, url=url, date=datetime_object)
            # for news in news_sections:
            #     news = news.strip()
            #     if news != "":
            #         self.log(news)
        except KeyError:
            self.error(response.meta.get('ticker'))

