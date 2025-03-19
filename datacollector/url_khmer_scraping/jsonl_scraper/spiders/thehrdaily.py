"""
Scrapy Spider for The HR Daily News.
Crawls thehrdaily website for articles
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class ThehrdailySpider(scrapy.Spider, PaginationHandle):
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
    start_urls: str
        URLs where the spider will begin to crawl from.
        The first pages downloaded will be those listed here.
        The subsequent request will be generated successively
        from data contained in the start URLs.
    """
    name = "thehrdaily"
    allowed_domains = ["thehrdaily.com"]
    base_url = "https://www.thehrdaily.com"
    start_urls = [f"{base_url}/management-and-leadership/page/25",
                  f"{base_url}/hr/",
                  f"{base_url}/training/",
                  f"{base_url}/hr/labour-law/",
                  f"{base_url}/personal-development/",
                  f"{base_url}/short-story/",
                  f"{base_url}/general-knowledge/",
                  f"{base_url}/ideas/",
                  f"{base_url}/scholars-and-famous-people/",
                  f"{base_url}/technology/",
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

        Attributes
        ---------
        articles: list
            Stores the desired article links when scraping from a website.
        current_page: str
            Stores the current page being scraped.
        next_page_url: str
            Stores the pagination link for Scrapy to follow.
        yields: str
            Yield the next page as well as callbacks to parse data and callbacks recursively.
        """
        articles = response.css(".entry-header .entry-title a::attr(href)").getall()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            current_url = response.url
            next_page = self.get_next_page_url(current_url)
            if next_page:
                # follow the next page url
                yield response.follow(next_page, self.parse)

    def parse_data(self, response):
        """
        This method for parse_data of `thehrdaily.com` to extracts
        the following details from the response:
            - category: The category get .entry-meta .cat-links of articles
            - title: extract from entry-title class of the post
            - content: The combined text content of the post.
            - url: the URL of the articles

        Yields:
            ScrapyItem: An item containing the extracted title, content, and URL of the article.
        """
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")
        item = ScrapyItem()
        item["category"] = ",".join(response.css(".entry-meta .cat-links a::text").getall())
        item["title"] = response.css("h1.entry-title ::text").get()
        item["content"] = "".join(response.css(".entry-content p ::text").getall())
        item["url"] = result

        yield item
