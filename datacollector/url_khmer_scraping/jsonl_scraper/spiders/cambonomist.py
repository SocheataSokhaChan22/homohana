"""
Scrapy Spider for Cambonomist.
Crawls the Khmer Cambonomist website for articles.
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class CambonomistSpider(scrapy.Spider, PaginationHandle):
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
    name = "cambonomist"
    allowed_domains = ["cambonomist.com"]
    base_url = "https://cambonomist.com"
    start_urls = [f"{base_url}/news/",
                  f"{base_url}/articles/",
                  f"{base_url}/popular/",
                  f"{base_url}/photos/stories/",
                  ]

    def parse(self, response, **kwargs):
        """
        This function is called for each item in the feed.
        Extracts article URLs from the current page and handles pagination.

        Attributes:
        articles: list
            Stores the desired article links when scraping from a website.
        current_url: str
            Stores the current URL being scraped.
        next_page: str
            Stores the pagination link for Scrapy to follow.
        Yields:
            scrapy.http.Request: Request for each article URL and the next page URL.
        Pagination Handling:
            - Increments the `page` parameter if present.
            - Defaults to `page=2` if no `page` parameter is found.
        """
        articles = response.css("#main a.titlelink::attr(href)").getall()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            next_page = response.css("ul.pager li.previous a::attr(href)").get()
            if next_page:
                current_url = response.url
                next_page_url = self.get_next_page_url_with_param(current_url)
                yield response.follow(next_page_url, callback=self.parse)

    def parse_data(self, response):
        """
        `Parse` method processes the given response from Cambonomist
        and extracting specific elements from the HTML. It retrieves
        the category, title, content, and URL of the article and yields the
        data as a ScrapyItem.

        Yields (ScrapyItem): An item containing the extracted data:
            - category (list): A list of categories.
            - title (str): The title of the article.
            - content (str): The main content of the article.
            - url (str): The URL of the response.
        """
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")
        item = ScrapyItem()
        item["category"] = response.css("div.alt-title ::text").get()
        item["title"] = response.css("div.page-article h1.title ::text").get()
        all_text = response.css(".page-article .excerpt ::text, .paragraph p ::text").getall()
        item["content"] = all_text
        item["url"] = result

        yield item
