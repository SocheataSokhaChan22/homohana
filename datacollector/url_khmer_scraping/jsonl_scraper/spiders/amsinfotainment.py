"""
Scrapy Spider for AMS infomation and Entertainment Website Cambodia.
Crawls the infotainment.ams.com.kh website for articles.
"""
import scrapy
from ..items import ScrapyItem


class AMSinfotainmentSpider(scrapy.Spider):
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
    name = "amsinfotainment"
    allowed_domains = ["infotainment.ams.com.kh"]
    base_url = "https://infotainment.ams.com.kh/category/"
    start_urls = [f"{base_url}/celebrity/news",
                  f"{base_url}/movie-and-music/news/",
                  f"{base_url}/reaction/news",
                  f"{base_url}/strange/news/",
                  f"{base_url}/food-and-hang-out/news",
                  f"{base_url}/life-style-love-and-relation/news/",
                  f"{base_url}/diy/news/",
                  f"{base_url}/life-style-health-and-beauty/news/",
                  f"{base_url}/life-style/hobbies/news",
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
        articles = response.css(".article__summary .article__title a::attr(href)").getall()
        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            next_page = response.css("nav.pagination a.next::attr(href)").get()
            # Handle pagination for infotainment.ams.com.kh
            if next_page:
                yield response.follow(next_page, self.parse)

    def parse_data(self, response):
        """
        This parsing data for infotainment.ams.com.kh Website.
        This method extracts the following details from the response:
        - category: The category of the post
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
        category = response.css(".article__meta .article__categories a::text").getall()
        item["category"] = ",".join(category)
        item["title"] = response.css("header.article__header h2.article__title::text").get()
        item["content"] = "".join(response.css("div.article__content p::text").getall())
        item["url"] = result

        yield item
