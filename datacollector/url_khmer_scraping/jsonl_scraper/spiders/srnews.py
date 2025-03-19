"""
Scrapy Spider for SR News.

Crawls the SR News website for articles
"""
import scrapy
from ..items import ScrapyItem


class SrnewsSpider(scrapy.Spider):
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
    name = "srdigitalmedia"
    allowed_domains = ["srdigitalmedia.com.kh"]
    base_url = "https://www.srdigitalmedia.com.kh"
    start_urls = [f"{base_url}/lifestyle/",
                  f"{base_url}/technology/",
                  f"{base_url}/knowledge/",
                  f"{base_url}/travel/",
                  f"{base_url}/business/",
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
            Stores the desired article links when scraping from a website
        next_page_url: str
            Stores the pagination link for Scrapy to follow
        yields: str
            Yield the next page as well as callbacks to parse data and callbacks recursively
        """
        articles = response.css(".div-block-91 div[role='listitem'] a::attr(href)").getall()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            next_page = response.css("a[aria-label='Next Page']::attr(href)").get()
            if next_page:
                next_page_url = response.urljoin(next_page)
                yield response.follow(next_page_url, self.parse)

    def parse_data(self, response):
        """
        This function handles the parsing of data by transforming the link into
        the JSONL format. The function also filters in order to extract only the
        necessary data.

        Parameters
        ---------
        response:
            response detail link from parse method

        Yields
        ---------
        item: dict
            A dictionary containing the extracted data in JSON format
        """
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")

        if "articles/" in result:
            item = ScrapyItem()
            item["category"] = response.css("div.detail-headline-block .heading-36::text").get()
            item["title"] = response.css("div.detail-headline-block h1::text").get()
            item["content"] = "".join(response.css("div.w-richtext p::text").getall())
            item["url"] = result

            yield item
