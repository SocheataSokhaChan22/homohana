"""
Scrapy Spider for ប្រជាប្រិយ Website Cambodia.
Crawls the Popoluar website for articles.
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class PopularkhSpider(scrapy.Spider, PaginationHandle):
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
    start_urls: str
        URLs where the spider will begin to crawl from.
        The first pages downloaded will be those listed here.
        The subsequent request will be generated successively
        from data contained in the start URLs.
    """
    name = "popularkh"
    allowed_domains = ["popular.com.kh"]
    base_url = "https://www.popular.com.kh/category"
    start_urls = [f"{base_url}/entertainment/",
                  f"{base_url}/social/",
                  f"{base_url}/sport/",
                  f"{base_url}/tours/",
                  f"{base_url}/strange-stories/",
                  f"{base_url}/mak-talk/",
                  f"{base_url}/fashion/",
                  f"{base_url}/lifejob/",
                  f"{base_url}/sponsored/",
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
            Stores the pagination link for Scrapy to follow.
        yields: str
            Yield the next page as well as callbacks to parse data and callbacks recursively.
        """
        articles = response.css(".post .post-heading a::attr(href)").getall()
        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            current_page = response.url
            # Handle pagination for opoluar website
            next_page = self.get_next_page_url(current_page)
            if next_page:
                yield response.follow(next_page, self.parse)

    def parse_data(self, response):
        """
        This function handles the parsing of data from popular.com.kh by
        transforming the link into the item and store in MongoDB.

        Args:
            response (scrapy.http.Response): The response object containing
            the HTML of the page to parse.

        Yields:
            ScrapyItem: An item containing the extracted title, content, and URL of the article.
        """
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")

        item = ScrapyItem()
        item["category"] = response.css(".category-single-post .post-cat span::text").get().strip()
        item["title"] = response.css("div.entry-content h1.entry-title ::text").get()
        all_text = "".join(response.css(".post-body .entry-content p::text").getall())
        item["content"] = all_text
        item["url"] = result

        yield item
