"""
Scrapy Spider for Health Time Cambodia.
Crawls the Healthtime website for articles.
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class HealthtimeSpider(scrapy.Spider, PaginationHandle):
    """
    A scrapy spider class inherited from the scrapy library.

    Attribute
    ----------
    name: : str
        A string which defines the name for this spider.
    allowed_domain: str
        An optional list of strings containing domains that this
        spider is allowed to crawl. Requests for URLs not belonging
        to the domain names specified in this list (or their subdomains) will not
        be followed.
    base_url: The base URL of category of the website.
    start_urls: str
        URLs where the spider will begin to crawl from.
        The first pages downloaded will be those listed here.
        The subsequent request will be generated successively
        from data contained in the start URLs.
    """
    name = "healthtime"
    allowed_domains = ["healthtime.tips"]
    start_urls = ["https://www.healthtime.tips/km/library/articles"]

    def parse(self, response, **kwargs):
        """
        This function is called for each item in the feed.
        Extracts article URLs from the current page and handles pagination.

        Attributes:
        articles: list
            Stores the desired article links when scraping from a website.
        current_url: str
            Stores the current URL being scraped.
        next_page_url: str
            Stores the pagination link for Scrapy to follow.
        Yields:
            scrapy.http.Request: Request for each article URL and the next page URL.
        """
        articles = response.css(".mb-2.nav-dark .nav-link::attr(href)").getall()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            current_url = response.url
            next_page_url = self.get_next_page_url_with_param(current_url)
            if next_page_url:
                yield response.follow(next_page_url, self.parse)

    def parse_data(self, response):
        """
        This function handles the parsing of data from `HealthTime`
        website and extracting specific elements.

        Yields (ScrapyItem): An item containing the extracted data:
            - category (list): A list of categories.
            - title (str): The title of the article.
            - content (str): The main content of the article.
            - url (str): The URL of the response.
        """
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")
        item = ScrapyItem()
        item["category"] = response.css("a.cs-tag ::text").get()
        item["title"] = response.css("h1.mb-4.pb-1 ::text").get()
        item["content"] = "".join(response.css(".container .col-md-8 p ::text").getall())
        item["url"] = result
        yield item
