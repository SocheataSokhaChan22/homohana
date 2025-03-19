"""
Scrapy Spider for AMS Economy Website Cambodia.
Crawls the AMS Economy website for articles.
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class AMSEconomySpider(scrapy.Spider, PaginationHandle):
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
    name = "amseconomy"
    allowed_domains = ["economy.ams.com.kh"]
    base_url = "https://economy.ams.com.kh/category/all-news"
    start_urls = [f"{base_url}/news-economic/",
                  f"{base_url}/news-finance/",
                  f"{base_url}/news-realestate/",
                  f"{base_url}/news-business/",
                  f"{base_url}/news-pr/",
                  f"{base_url}/news-startup-and-innovation",
                  ]

    def parse(self, response, **kwargs):
        """
        This method is the default callback used by Scrapy to handle
        responses and manages paginations.

        Attributes
        ----------
        articles : list
            A list that stores the desired article links extracted from the response.
        next_page : str
            A string representing the pagination link for Scrapy to follow,
            extracted using a CSS selector.
        Yields
        ------
        scrapy.http.Request
        """
        articles = response.css(".articles .article__attachment--thumbnail a::attr(href)").getall()
        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            next_page = self.get_next_page_url(response.url)
            if next_page:
                # Following the next page
                yield response.follow(next_page, self.parse)

    def parse_data(self, response):
        """
        Parse the response data from AMS Economy and return a Scrapy item.
        This method extracts specific information from the given response,
        including the article's categories, title, content, and URL,

        Yields
        ------
        item : ScrapyItem
            A dictionary containing the extracted data in JSON format, which includes:
        category : str
            A comma-separated string of categories associated with the article.
        title : str
            The title of the article.
        content : str
            The main content of the article, concatenated from all paragraph texts.
        url : str
            The URL of the article.
        """
        item = ScrapyItem()
        self.logger.info(f"A response from {response.url} just arrived!")
        result = response.url
        category = response.css('.single-article__inner .article__categories a::text').getall()
        item["category"] = ",".join(category)
        item["title"] = response.css(".single-article__inner h2.entry-title ::text").get()
        all_text = "".join(response.css(".article__content p::text").getall())
        item["content"] = all_text
        item["url"] = result

        yield item
