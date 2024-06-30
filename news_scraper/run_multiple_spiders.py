import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Import your spiders
from news_scraper.spiders.scrape_mc import McScraperSpider
from news_scraper.spiders.livemint_scraper import LivemintScraperSpider
from news_scraper.spiders.scrape_et import ScrapeEtSpider

# Get Scrapy settings
settings = get_project_settings()

# Initialize CrawlerProcess with settings
process = CrawlerProcess(settings)

# Add your spiders to the process
process.crawl(McScraperSpider)
process.crawl(LivemintScraperSpider)
process.crawl(ScrapeEtSpider)

# Start the crawling process
process.start()  # This will block until all crawlers are finished
