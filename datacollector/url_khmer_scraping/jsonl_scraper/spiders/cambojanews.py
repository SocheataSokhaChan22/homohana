"""
Scrapy Spider for Khmer Camboja News.

Crawls the Khmer Camboja News website for articles
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class CambojaSpider(scrapy.Spider, PaginationHandle):
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
    name = "cambojanews"
    allowed_domains = ["khmer.cambojanews.com"]
    base_url = "https://khmer.cambojanews.com/category"
    start_urls = [f"{base_url}/journalists/",
                  f"{base_url}/politic/",
                  f"{base_url}/social/",
                  f"{base_url}/environment/",
                  f"{base_url}/human-right/",
                  f"{base_url}/business/",
                  f"{base_url}/opinion/",
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
        articles = response.css("a.ee-post__title ::attr(href)").getall()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            current_page = response.url
            next_page = self.get_next_page_url(current_page)
            if next_page:
                yield response.follow(next_page, self.parse)

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

        item = ScrapyItem()
        item["category"] = response.css("span.elementor-post-info__terms-list a::text").getall()
        item["title"] = response.css("div.elementor-widget-container h1::text").get()
        all_text = "".join(response.css("div.elementor-widget-container p::text").getall())
        item["content"] = all_text
        item["url"] = result

        yield item
