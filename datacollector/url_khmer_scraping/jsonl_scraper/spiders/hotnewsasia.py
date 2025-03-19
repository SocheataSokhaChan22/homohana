"""
Scrapy Spider for Hot News Asia.

Crawls the Hot News Asia website for articles
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class HotnewsasiaSpider(scrapy.Spider, PaginationHandle):
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
    name = "hotnewasia"
    allowed_domains = ["hotnews-asia.com"]
    base_url = "https://www.hotnews-asia.com/detail/category"
    start_urls = [
        f"{base_url}/national/",
        f"{base_url}/internastional/",
        f"{base_url}/នយោបាយ/",
        f"{base_url}/បទវិភាគ/",
        f"{base_url}/ប្រវត្តិសាស្ត្រ/",
        f"{base_url}/ធុរកិច្ច/",
        f"{base_url}/សុខភាព-និងកីឡា/",
        f"{base_url}/covid-19/"
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
        next_page: str
            Stores the pagination link for Scrapy to follow
        yields: str
            Yield the next page as well as callbacks to parse data and callbacks recursively
        """
        articles = response.css(".listing-blog > article h2.title a::attr(href)").getall()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            url_parts = response.url
            next_page_url = self.get_next_page_url(url_parts)
            if next_page_url:
                yield response.follow(next_page_url, self.parse)

    def parse_data(self, response):
        """
        Parses the data from the response and extracts the relevant information.

        This method processes the response received from the URL, logs the URL,
        and checks if the URL contains "archives/" then extracts the title and
        content of the article and yields the item.

        Args:
            response (scrapy.http.Response): The response object containing
            the HTML of the page to parse.

        Yields:
            ScrapyItem: An item containing the extracted title, content, and URL of the article.
        """

        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")

        if "detail/" in result:
            item = ScrapyItem()
            item["category"] = response.css("div.term-badges span.term-badge ::text").getall()
            item["title"] = response.css("h1.single-post-title span.post-title::text").get()
            all_text = "".join(response.css("div.entry-content p::text").getall())
            item["content"] = all_text
            item["url"] = result

            yield item
