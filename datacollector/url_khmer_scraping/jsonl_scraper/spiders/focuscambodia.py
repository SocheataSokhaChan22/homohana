"""
Scrapy Spider for Focus Cambodia.
Crawls the Khmer Focus Cambodia website for articles.
"""
import scrapy
from ..items import ScrapyItem


class FocuscambodiaSpider(scrapy.Spider):
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
    name = "focuscambodia"
    allowed_domains = ["focus-cambodia.com"]
    base_url = "https://focus-cambodia.com/km/"
    start_urls = [f"{base_url}/អាជីព/",
                  f"{base_url}/គួរដឹង/",
                  f"{base_url}/ផែនដី/",
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
            - Increments the number page if present.
            - Defaults to `/2` if no `page` parameter is found.
        """
        css_selector = ".elementor-element-9743a67 .elementor-post__title a::attr(href)"
        articles = response.css(css_selector).getall()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            current_url = response.url.rstrip("/").split("/")
            if current_url[-1].isdigit():
                current_url[-1] = str(int(current_url[-1]) + 1)
            else:
                current_url.append("/2")
            next_page_url = "/".join(current_url)

            if next_page_url:
                yield response.follow(next_page_url, self.parse)

    def parse_data(self, response):
        """
        `Parse` method processes the given response from FocusCambodia
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
        item["category"] = ",".join(response.css(".entry-meta a::text").getall())
        item["title"] = response.css("h1.entry-title ::text").get()
        item["content"] = "".join(response.css(".entry-content ::text").getall())
        item["url"] = result
        yield item
