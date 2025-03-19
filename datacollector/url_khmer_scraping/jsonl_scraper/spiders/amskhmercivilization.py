"""
Scrapy Spider for AMS Khmer Civilization Website Cambodia.
Crawls the Khmer Civilization website for articles.
"""
import scrapy
from ..items import ScrapyItem


class AMSkhmercivilizationSpider(scrapy.Spider):
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
    base_url: str
        The base URL of category of the website.
    new_url: str
        The URL of category `news` of the website.
    start_urls: str
        URLs where the spider will begin to crawl from.
        The first pages downloaded will be those listed here.
        The subsequent request will be generated successively
        from data contained in the start URLs.
    """
    name = "amskhmercivilization"
    allowed_domains = ["ams.com.kh"]
    base_url = "https://ams.com.kh/khmercivilization"
    start_urls = [f"{base_url}/history/archaeology",
                  f"{base_url}/history/art-history",
                  f"{base_url}/history/inscription",
                  f"{base_url}/traditionals/belief",
                  f"{base_url}/traditionals/rule",
                  f"{base_url}/traditionals/handicraft",
                  f"{base_url}/chronicle/អក្សរសិល្ប៍",
                  f"{base_url}/arts/living-heritage",
                  f"{base_url}/arts/plays",
                  f"{base_url}/arts/musics",
                  f"{base_url}/arts/khmer-architecture",
                  f"{base_url}/entertain/pop-game",
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
        next_page: str
            Stores the pagination link for Scrapy to follow using css selector.
        yields: str
            Yield the next page as well as callbacks to parse data and callbacks recursively.
        """
        articles = response.css(".td-module-meta-info h3.entry-title a::attr(href)").getall()
        category = response.css("div.td-image-container .td-post-category::text").get()
        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data, cb_kwargs={"category": category})

            next_page = response.css(".page-nav a[aria-label='next-page']::attr(href)").get()
            # Handle pagination for khmercivilization
            if next_page:
                yield response.follow(next_page, self.parse)

    def parse_data(self, response, category):
        """
        This parsing data for khmercivilization Website.
        This method extracts the following details from the response:
        - category: The category get from the post articles
        - title: The title of the post
        - content: The combined text content of the post.

        Yields
        ---------
        item (ScrapyItem): dict
            A dictionary containing the extracted data in JSON format
        """
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")

        item = ScrapyItem()
        item["category"] = category
        item["title"] = response.css("h1 ::text").get()
        item["content"] = "".join(response.css("p::text").getall())
        item["url"] = result

        yield item
