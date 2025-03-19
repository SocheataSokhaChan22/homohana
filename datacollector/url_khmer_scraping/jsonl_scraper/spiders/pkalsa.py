"""
Scrapy Spider for PkaSla.
Crawls the Khmer PKASLA website for articles
"""
import scrapy
from ..items import ScrapyItem


class PkaslaSpider(scrapy.Spider):
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
    name = "pkasla"
    allowed_domains = ["pkaslatv.com"]
    base_url = "https://www.pkaslatv.com/category"
    start_urls = [f"{base_url}/បច្ចេកវិទ្យា/",
                  f"{base_url}/កសិកម្ម-ទេសចរណ៍/",
                  f"{base_url}/អចលនទ្រព្យ/",
                  f"{base_url}/សង្គម-ជីវិត/",
                  f"{base_url}/ភាពយន្ត-កម្សាន្ត/",
                  f"{base_url}/វប្បធម៌-សិល្បៈ/",
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
        articles = response.css("article.item h2.entry-title a::attr(href)").getall()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            next_page_url = response.css(".penci-pagination .page-numbers a.next::attr(href)").get()

            if next_page_url:
                yield response.follow(next_page_url, callback=self.parse)

    def parse_data(self, response):
        """
        This parsing data for Pkasla Website.
        This method extracts the following details from the response:
            - category: The category get from the post articles
            - title: The title of the post
            - content: The combined text content of the post.
            - url: the URL of the articles

        Yields:
            ScrapyItem: An item containing the extracted title, content, and URL of the article.
        """
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")

        item = ScrapyItem()
        item["category"] = ",".join(response.css("div.penci-standard-cat .cat a ::text").getall())
        item["title"] = response.css("div.single-header h1.post-title ::text").get()
        item["content"] = "".join(response.css("div.post-entry .entry-content p ::text").getall())
        item["url"] = result

        yield item
