"""Simple Script to Run Spiders Simultaneously"""
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Import all spiders
from url_khmer_scraping.jsonl_scraper.spiders.newsroom import NewsroomSpider

# set up the Crawler Setting
settings = get_project_settings()

# Initalize and set up the Crawler Process
process = CrawlerProcess(settings)

# Add spiders to process and start scraping
process.crawl(NewsroomSpider)

# This blocks until all crawling jobs are finished
process.start()
