"""
Scrapy Spider for Mediabrandbodia.
Crawls the Khmer media.brandbodia.com website for articles.
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class MediabrandbodiaSpider(scrapy.Spider, PaginationHandle):
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
    name = "brandbodia"
    allowed_domains = ["media.brandbodia.com"]
    base_url = "https://media.brandbodia.com/article/category"
    start_urls = [f"{base_url}/ព័ត៌មានទូទៅ/របៀបរស់នៅ/",
                  f"{base_url}/ព័ត៌មានទូទៅ/នយោបាយ/",
                  f"{base_url}/ព័ត៌មានទូទៅ/សង្គម/",
                  f"{base_url}/ព័ត៌មានអន្តរជាតិ/",
                  f"{base_url}/ព័ត៌មានកម្សាន្ត/សិល្បៈ/",
                  f"{base_url}/ព័ត៌មានកម្សាន្ត/កម្សាន្ត/",
                  f"{base_url}/gn-news/បច្ចេកវិទ្យា/",
                  f"{base_url}/gn-news/កីឡា/",
                  f"{base_url}/gn-news/របកគំហើញ/",
                  f"{base_url}/gn-news/បរិស្ថាន/",
                  f"{base_url}/gn-news/សុខភាព/",
                  f"{base_url}/ទស្សនៈយុវជន/",
                  f"{base_url}/ពាណិជ្ជកម្ម/",
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
            - Increments the `page` parameter if present.
            - Defaults to `page=2` if no `page` parameter is found.
        """
        articles = response.css("article.entry a.post-thumbnail::attr(href)").getall()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            next_page = response.css("div.nav-links .next::attr(href)").get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)

    def parse_data(self, response):
        """
        `Parse` method processes the given response from Mediabrandbodia
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
        category = response.css(".entry-taxonomies .category-links a::text").getall()
        item["category"] = ",".join(category)
        item["title"] = response.css("h1.entry-title ::text").get()
        item["content"] = "".join(response.css("div.entry-content p ::text").getall())
        item["url"] = result

        yield item
