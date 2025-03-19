"""
Scrapy Spider for Karpit Website
Crawls the Karpit News website for articles
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class KarpitSpider(scrapy.Spider, PaginationHandle):
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
    name = "karpit"
    custom_settings = {
        "FEEDS": {
            "output/karpit.jsonl":
            {
                "format": "jsonlines"
            },
        },
        "FEED_EXPORT_ENCODING": "utf-8"
    }
    allowed_domains = ["karpit.news"]
    base_url = "https://www.karpit.news/category"
    start_urls = [f"{base_url}/international",
                  f"{base_url}/analysis",
                  f"{base_url}/opinion",
                  f"{base_url}/politics",
                  f"{base_url}/society",
                  f"{base_url}/entertainment",
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
        articles = response.css("#primary .entry-title a::attr(href)").getall()
        category = response.css(".post-categories a::text").get()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data, cb_kwargs={"category": category})

            next_page_url = response.css(".nav-links .next::attr(href)").get()
            if next_page_url:
                yield response.follow(next_page_url, callback=self.parse)

    def parse_data(self, response, category):
        """
        Parses the data from the response and extracts the relevant information.

        This method processes the response received from the URL, logs the URL,
        and checks if the URL contains "archives/" then extracts the title and
        content of the article and yields the item.

        Args:
            response (scrapy.http.Response): The response object containing
            the HTML of the page to parse.

        Yields:
            ScrapyItem: An item containing the extracted title, content, and URL of the article.
        """

        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")

        item = ScrapyItem()
        item["category"] = category
        item["title"] = response.css("header.entry-header h1 ::text").get()
        item["content"] = response.css(".entry-content p ::text").getall()
        item["url"] = result

        yield item
