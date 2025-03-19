"""
Scrapy Spider for Komnit Website
Crawls the Kumnit.com website for articles
"""
import scrapy
from ..items import ScrapyItem


class KumnitSpider(scrapy.Spider):
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
    name = "kumnit"
    allowed_domains = ["kumnit.com"]
    base_url = "https://kumnit.com/Topic"
    start_urls = [f"{base_url}/business/",
                  f"{base_url}/marketing/យុទ្ធសាស្ត្រទីផ្សារឌីជ/",
                  f"{base_url}/យុទ្ធសាស្ត្រលក់/",
                  f"{base_url}/business/អាជីវកម្មកំពុងពេញនិយម/",
                  f"{base_url}/business/គ្រប់គ្រង/",
                  f"{base_url}/ភាពជាអ្នកដឹកនាំ/",
                  f"{base_url}/business/ធុរកិច្ច%e2%80%8bអន្តរជាតិ/",
                  f"{base_url}/កសិកម្ម/",
                  f"{base_url}/ហិរញ្ញវត្ថុ/",
                  f"{base_url}/technology/",
                  f"{base_url}/real_estate/",
                  f"{base_url}/អភិវឌ្ឍន៍ខ្លួនឯង/",
                  f"{base_url}/application/",
                  f"{base_url}/សេដ្ឋកិច្ច/",
                  f"{base_url}/tumnongta/",
                  f"{base_url}/kumnitplus/",
                  ]

    def parse(self, response, **kwargs):
        """
        This function handles the processing of downloaded responses.
        The default callback used by Scrapy.

        Parameters
        ---------
        response:
            An object that represents an HTTP response, which is usually downloaded
            (by the Downloader) and fed to the Scrapy spiders for processing
        get_next_page_url_with_param:
            A function that returns the next page URL with the given parameter.
        Attributes
        ---------
        articles: list
            Stores the desired article links when scraping from a website
        next_page: str
            Stores the pagination link for Scrapy to follow
        yields: str
            Yield the next page as well as callbacks to parse data and callbacks recursively
        """
        articles = response.css(".tdb-block-inner h3.entry-title a::attr(href)").getall()

        if articles:
            for article in articles:
                yield response.follow(article, callback=self.parse_data)

            next_page_url = response.css(".page-nav a[aria-label='next-page']::attr(href)").get()
            # Handle pagination for kumnit
            if next_page_url:
                yield response.follow(next_page_url, callback=self.parse)

    def parse_data(self, response):
        """
        This parsing data for Kumnit Website.
        This method extracts the following details from the response:
            - category: The category get from the post articles
            - title: The title of the post
            - content: The combined text content of the post.
            - url: the URL of the articles

        Yields:
            ScrapyItem: An item containing the extracted title, content, and URL of the article.
        """

        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")

        item = ScrapyItem()
        category_selector = ".tdb-category .tdb-entry-category::text, .entry-category ::text"
        content = ".tdb-block-inner p ::text, .td-post-content p ::text"
        item["category"] = ",".join(response.css(category_selector).getall())
        item["title"] = response.css("h1.tdb-title-text ::text, h1.entry-title ::text").get()
        item["content"] = "".join(response.css(content).getall())
        item["url"] = result

        yield item
