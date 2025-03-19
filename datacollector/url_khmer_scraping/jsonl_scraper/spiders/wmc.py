"""
Scrapy Spider for Women Media Centre of Cambodia.
Crawls the WMC Organization website for articles
"""
import scrapy
from ..items import ScrapyItem


class WMCSpider(scrapy.Spider):
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
    name = "wmckh"
    allowed_domains = ["wmc.org.kh"]
    base_url = "https://wmc.org.kh"
    start_urls = [f"{base_url}/ព័ត៌មានជាតិ/",
                  f"{base_url}/ព័ត៌មានអន្តរជាតិ/",
                  f"{base_url}/ព័ត៌មានដែលបានផ្ទៀងផ្ទា/",
                  f"{base_url}/ស្ត្រីក្នុងបច្ចុប្បន្ន/",
                  f"{base_url}/បទរាយការណ៍/",
                  f"{base_url}/បទសម្ភាសន៍/",
                  f"{base_url}/បទវិភាគ/",
                  f"{base_url}/សេដ្ឋកិច្ច/",
                  f"{base_url}/សំឡេងយុវជន/",
                  f"{base_url}/នាទីសុខភាព/",
                  ]

    def parse(self, response, **kwargs):
        """
        `Parse` method extracts article URLs from the website and
        yields requests to follow these URLs. It also handles pagination.

        Attributes
        ----------
        articles : list
            A list of article URLs extracted from the current page.
        next_page : str
            The URL of the next page, if pagination is present.

        Yields
        ------
        scrapy.Request
            Requests to follow each article URL, calling
            `parse_data` to handle individual articles.
        scrapy.Request
            A request to follow the next page if a 'next'
            pagination link is found, calling `parse` recursively.
        """
        articles = response.css(".elementor-post__title a::attr(href)").getall()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            next_page = response.css("nav.elementor-pagination .next::attr(href)").get()
            if next_page:
                yield response.follow(next_page, self.parse)

    def parse_data(self, response):
        """
        This method processes the response of an individual article page,
        extracts relevant data, and yields the result as a Scrapy item.

        Attributes
        ----------
        result : str
            The URL of the current article page.
        item : ScrapyItem
            The Scrapy item storing the extracted data fields.

        Yields
        ------
        ScrapyItem
            The scraped data, including category, title, content, and the article URL.
        """
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")

        item = ScrapyItem()
        category = response.css(".elementor-post-info__terms-list ::text").getall()
        item["category"] = ",".join(category)
        item["title"] = response.css(".elementor-page-title .elementor-size-default ::text").get()
        item["content"] = "".join(response.css(".elementor-widget-container p ::text").getall())
        item["url"] = result

        yield item
