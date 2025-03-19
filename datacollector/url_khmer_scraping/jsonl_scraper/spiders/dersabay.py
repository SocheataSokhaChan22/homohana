"""
Scrapy Spider for Der Sabay.
Crawls the der.sabay.com.kh website for articles
"""
import scrapy
from ..items import ScrapyItem


class DersabaySpider(scrapy.Spider):
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
    name = "dersabay"
    allowed_domains = ["der.sabay.com.kh"]
    base_url = "https://der.sabay.com.kh/topics"
    base_ajax = "https://der.sabay.com.kh/ajax/topics"
    start_urls = [f"{base_url}/hang-out",
                  f"{base_url}/food-and-drink",
                  f"{base_url}/fashion",
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
        articles = response.css(".item a::attr(href)").getall()
        if articles:
            for article in articles:

                yield response.follow(article, self.parse_data)

            current_url = response.url.rstrip("/").split("/")
            if current_url[-1].isdigit():
                current_url[-1] = str(int(current_url[-1]) + 1)
                ajax_url = "/".join(current_url)
            else:
                category_name = response.url.split("/")[-1]
                ajax_url = f"{self.base_ajax}/{category_name}/2"

            yield scrapy.FormRequest(
                url=ajax_url,
                method="GET",
                callback=self.parse,
            )

    def parse_data(self, response):
        """
        This parsing data for DerSabay Website.
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
        item["category"] = ",".join(response.css(".post_tags .tag ::text").getall())
        item["title"] = response.css(".header .title ::text").get()
        item["content"] = "".join(response.css("#post_content p ::text").getall())
        item["url"] = result

        yield item
