"""
Scrapy Spider for Kangea24.
Crawls the Khmer Kangea24.com website for articles
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class Kangea24Spider(scrapy.Spider, PaginationHandle):
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
    name = "kangea24"
    allowed_domains = ["kangea24.com"]
    base_url = "https://kangea24.com/categories"
    start_urls = [f"{base_url}/1/",
                  f"{base_url}/6/",
                  f"{base_url}/7/",
                  f"{base_url}/8/",
                  f"{base_url}/9/",
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
        next_page_url: str
            Stores the pagination link for Scrapy to follow.
        yields: str
            Yield the next page as well as callbacks to parse data and callbacks recursively.
        """
        articles = response.css("div.trand-right-cap a::attr(href)").getall()
        category = response.css("div.trand-right-cap span::text").get()
        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data, cb_kwargs={"category": category})

            current_url = response.url
            next_page = self.get_next_page_url_with_param(current_url)

            if next_page:
                yield response.follow(next_page, callback=self.parse)

    def parse_data(self, response, category):
        """
        This parsing data for Kangea24 Website.
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
        item["category"] = category
        item["title"] = response.css("div.section-tittle h4 ::text").get()
        item["content"] = "".join(response.css(".about-right p ::text").getall())
        item["url"] = result

        yield item
