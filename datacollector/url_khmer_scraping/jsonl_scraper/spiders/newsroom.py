"""
Scrapy Spider for NewsRoom Cambodia

Crawls the NewsRoom Cambodia website for articles
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class NewsroomSpider(scrapy.Spider, PaginationHandle):
    """
    A scrapy spider class inherited from the scrapy library.

    Attribute
    ----------
    name: : str
        A string which defines the name for this spider.
    start_urls: str
        URLs where the spider will begin to crawl from.
        The first pages downloaded will be those listed here.
        The subsequent request will be generated successively
        from data contained in the start URLs.
    allowed_domain: str
        An optional list of strings containing domains that this
        spider is allowed to crawl. Requests for URLs not belonging
        to the domain names specified in this list (or their subdomains) will not
        be followed.
    custom_settings: dict
        configuration we can set up for an individual spider to alter the default settings.
        and Configure item pipelines and MongoDB settings
    """
    name = "newsroom"
    custom_settings = {
        "FEEDS": {
            f"output/{name}.jsonl":
            {
                "format": "jsonlines"
            },
        },
        "FEED_EXPORT_ENCODING": "utf-8"
    }
    allowed_domains = ["newsroomcambodia.com"]
    base_url = "https://newsroomcambodia.com/category"
    start_urls = [f"{base_url}/kh/",
                  f"{base_url}/group-vii/",
                  f"{base_url}/group-vi/",
                  f"{base_url}/group-xi/",
                  f"{base_url}/group-ix/",
                  ]

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
        jsonl_result: dict
            jsonl format of the article
        """
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")

        if "news/" in result or "kh/" in result:
            item = ScrapyItem()
            item["title"] = response.css("h1.entry-title ::text").get()
            all_text = "".join(response.css("div.td-post-content p::text").getall())
            item["content"] = all_text
            item["url"] = result

            yield item

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
        next_page: str
            Stores the pagination link for Scrapy to follow
        yields: str
            Yield the next page as well as callbacks to parse data and callbacks recursively
        """
        articles = response.css("h3[class='entry-title td-module-title'] ::attr(href)").getall()

        if articles:

            for article in articles:
                # check within the dict if has in dict we skip if not please move
                yield response.follow(article, self.parse_data)

            current_page = response.url
            next_page = self.get_next_page_url(current_page)
            if next_page:
                yield response.follow(next_page, callback=self.parse)
