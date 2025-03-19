"""
crapy settings for url_khmer_scraping project
"""
import os
# from dotenv import load_dotenv

# load_dotenv()

BOT_NAME = "url_khmer_scraping"
SPIDER_MODULES = ["jsonl_scraper.spiders"]
NEWSPIDER_MODULE = "url_khmer_scraping.spiders"

# ITEM_PIPELINES = {
#     "jsonl_scraper.pipelines.MongoDBPipeline": 300
# }

# MONGO_URI = os.environ.get("MONGO_URI")
# MONGO_DATABASE = os.environ.get("MONGO_DB_NAME")
# DOWNLOADER_MIDDLEWARES = {
#     "jsonl_scraper.middlewares.UrlKhmerScrapingSpiderMiddleware": 543,
# }

"""
Obey robots.txt rules
"""
ROBOTSTXT_OBEY = False

"""
# Set settings whose default value is deprecated to a future-proof value
"""
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
