"""
Scrapy Spider for AMS Education Website Cambodia.
Crawls the AMS Education website for articles.
"""
import scrapy
from ..items import ScrapyItem


class AMSEducationSpider(scrapy.Spider):
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
    name = "amseducation"
    allowed_domains = ["education.ams.com.kh"]
    base_url = "https://education.ams.com.kh/category/all-news"
    new_url = f"{base_url}/news-national-and-international-education-update"
    start_urls = [f"{new_url}/news-national-education",
                  f"{new_url}/news-international-education",
                  f"{base_url}/news-life-education",
                  f"{base_url}/news-skill-project",
                  f"{base_url}/news-outstdanding-youth",
                  f"{base_url}/news-children-education",
                  f"{base_url}/news-scholarships-news",
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
        articles = response.css(".articles .article__attachment--thumbnail a::attr(href)").getall()
        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            next_page = response.css("nav.pagination a.next::attr(href)").get()
            if next_page:
                yield response.follow(next_page, self.parse)

    def parse_data(self, response):
        """
        This function handles the parsing of data by
        transforming the link into the item and store in MongoDB.

        Parameters
        ---------
        response:
            response detail link from parse method

        Yields
        ---------
        item (ScrapyItem): dict
            A dictionary containing the extracted data in JSON format
        """
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")

        item = ScrapyItem()
        category = response.css('.single-article__inner .article__categories a::text').getall()
        item["category"] = ",".join(category)
        item["title"] = response.css("div.single-article__inner h2.entry-title ::text").get()
        all_text = "".join(response.css("div.article__content p::text").getall())
        item["content"] = all_text
        item["url"] = result

        yield item
