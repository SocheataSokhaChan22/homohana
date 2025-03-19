"""
Scrapy Spider for Kanhasabay Website
Crawls the Kanhasabay news for articles
"""
import scrapy
from ..items import ScrapyItem


class KanhasabaySpider(scrapy.Spider):
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
    name = "kanhasabay"
    allowed_domains = ["kanha.sabay.com.kh"]
    base_url = "https://kanha.sabay.com.kh/topics"
    start_urls = [f"{base_url}/news/",
                  f"{base_url}/healths/",
                  f"{base_url}/pregnancy/",
                  f"{base_url}/raising-children/",
                  f"{base_url}/disease/",
                  f"{base_url}/career/",
                  f"{base_url}/fashions/",
                  f"{base_url}/beauty/",
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
        next_page_url: str
            Stores the pagination link for Scrapy to follow.
        yields: str
            Yield the next page as well as callbacks to parse data and callbacks recursively.
        """
        category = response.url.rstrip("/").split("/")[-1]
        ajax_url = f"https://kanha.sabay.com.kh/ajax/topics/{category}/1"

        yield scrapy.FormRequest(
            url=ajax_url,
            method="GET",
            callback=self.parse_data_ajax,
            meta={"page": 1, "category": category},
        )

    def parse_data_ajax(self, response):
        """
        Processes the AJAX response to extract article URLs and handles pagination.

        Attributes
        ----------
        listings : str
            The raw HTML response in text format, representing the loaded article listings.
        selector : scrapy.Selector
            A Selector object used to extract data from the HTML text.
        articles : list of str
            A list of article URLs extracted from the AJAX response.
        page : int
            The current page number for pagination, extracted from the response metadata.
        category : str
            The category of articles being scraped, extracted from the response metadata.
        next_ajax_url : str
            The URL for the next page of articles (via AJAX request).

        Yields
        ------
        scrapy.http.Request
            Requests to follow individual article links.
        scrapy.http.FormRequest
            A GET request to the next AJAX page for the same category.
        """
        listings = response.text
        if listings:
            selector = scrapy.Selector(text=listings)
            articles = selector.css(".item a::attr(href)").getall()
            if articles:
                for article in articles:
                    yield response.follow(article, self.parse_data)

                page = response.meta["page"] + 1
                category = response.meta["category"]
                next_ajax_url = f"https://kanha.sabay.com.kh/ajax/topics/{category}/{page}"

                if len(articles) > 0:
                    yield scrapy.FormRequest(
                        url=next_ajax_url,
                        method="GET",
                        callback=self.parse_data_ajax,
                        meta={"page": page, "category": category},
                    )

    def parse_data(self, response):
        """
        Extracts detailed article data such as the category, title,
        content, and URL from an individual article page.

        Yields
        ------
        ScrapyItem
            The ScrapyItem object with the extracted article details.
        """
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")

        item = ScrapyItem()
        item["category"] = ",".join(response.css(".tag ::text").getall())
        item["title"] = response.css(".title p ::text").get()
        item["content"] = "".join(response.css(".content-detail p ::text").getall())
        item["url"] = result

        yield item
