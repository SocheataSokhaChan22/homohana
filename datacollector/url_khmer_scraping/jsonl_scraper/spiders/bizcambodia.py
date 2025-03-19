"""
Scrapy Spider for Biz Cambodia News.
Crawls Biz Cambodia website for articles
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class BizcambodiaSpider(scrapy.Spider, PaginationHandle):
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
    name = "bizcambodia"
    allowed_domains = ["bizkhmer.com"]
    base_url = "https://www.bizkhmer.com/categories"
    start_urls = [f"{base_url}/entrepreneurship/",
                  f"{base_url}/startup/",
                  f"{base_url}/Skills/",
                  f"{base_url}/ideas/",
                  f"{base_url}/Business/",
                  f"{base_url}/myproducts/",
                  f"{base_url}/Social/",
                  f"{base_url}/technology/",
                  f"{base_url}/real-estate/",
                  f"{base_url}/legal/",
                  f"{base_url}/specialarticles/",
                  f"{base_url}/press_release/",
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
        articles = response.css(".title-large a::attr(href)").getall()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            current_page = response.url
            next_page = self.get_next_page_url_with_param(current_page)
            if next_page:
                yield response.follow(next_page, self.parse)

    def parse_data(self, response):
        """
        This method for `Biz Cambodia` Website extracts the following details from the response:
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
        item["category"] = ",".join(response.css(".post-tags a::text").getall())
        item["title"] = response.css(".post-title-area .post-title ::text").get()
        item["content"] = "".join(response.css(".entry-content p ::text").getall())
        item["url"] = result

        yield item
