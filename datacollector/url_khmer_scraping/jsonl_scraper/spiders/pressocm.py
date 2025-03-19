"""
Scrapy Spider for Pressocm News.

Crawls the Pressocm News Cambodia website for articles
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class PressocmSpider(scrapy.Spider, PaginationHandle):
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
    name = "pressocm"
    allowed_domains = ["pressocm.gov.kh"]
    base_url = "https://pressocm.gov.kh/archives/category"
    start_urls = [f"{base_url}/opinion-political-kh/",
                  f"{base_url}/general-information-km/news-km/",
                  f"{base_url}/general-information-km/speech-km/",
                  f"{base_url}/general-news/message-km-km-en-km/",
                  f"{base_url}/general-information-km/press-release-km-km/",
                  f"{base_url}/general-information-km/report-km/",
                  f"{base_url}/general-information-km/asean-km/",
                  f"{base_url}/interview-km/",
                  f"{base_url}/general-information-km/mtns-kh/",
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
        category: str
            Stores the category of the website
        yields: str
            Yield the next page as well as callbacks to parse data and callbacks recursively
        """
        articles = response.css("h3[class='entry-title td-module-title'] ::attr(href)").getall()
        category = response.css("h1[class='entry-title td-page-title']::text").get()
        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data, cb_kwargs={"category": category})

            current_page = response.url
            next_page_url = self.get_next_page_url(current_page)
            if next_page_url:
                yield response.follow(next_page_url, self.parse)

    def parse_data(self, response, category):
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

        if "archives/" in result:
            item = ScrapyItem()
            item["category"] = category
            item["title"] = response.css("h1.tdb-title-text::text").get()
            all_text = "".join(response.css("div.tdb-block-inner.td-fix-index p::text").getall())
            item["content"] = all_text
            item["url"] = result

            yield item
