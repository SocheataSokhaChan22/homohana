"""
Scrapy Spider for Hello Krupet.

Crawls the Hello Krupet Cambodia website for articles.
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class HelloKrupetSpider(scrapy.Spider, PaginationHandle):
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
    name = "hellokrupet"
    custom_settings = {
        "FEEDS": {
            f"output/{name}.jsonl":
            {
                "format": "jsonlines"
            },
        },
        "FEED_EXPORT_ENCODING": "utf-8"
    }
    allowed_domains = ["hellokrupet.com"]
    base_url = "https://hellokrupet.com"
    start_urls = [f"{base_url}/លំហាត់ប្រាណ/",
                  f"{base_url}/ជំងឺកុមារ/",
                  f"{base_url}/ឱសថរុក្ខជាតិនិងថ្នាំបន្ទាប់បន្សំ/",
                  f"{base_url}/ទម្លាប់ល្អ/",
                  f"{base_url}/សុខភាពបេះដូង/",
                  f"{base_url}/សុខភាពផ្លូវដង្ហើម/",
                  f"{base_url}/ជំងឺមហារីក/",
                  f"{base_url}/ខួរក្បាលនិងប្រព័ន្ធប្រសាទ/",
                  f"{base_url}/ជំងឺឆ្លង/",
                  f"{base_url}/សុខភាពប្រព័ន្ធរំលាយអាហ/",
                  f"{base_url}/ជំងឺឆ្អឹងនិងសាច់ដុំ/",
                  f"{base_url}/សុខភាពប្រព័ន្ធទឹកនោម/",
                  f"{base_url}/ជំងឺឈាម/",
                  f"{base_url}/សុខភាពទូទៅ/",
                  f"{base_url}/សុខភាពភ្នែក/",
                  f"{base_url}/ជំងឺអាលែកហ្ស៊ី/",
                  f"{base_url}/ជំងឺត្រចៀក-ច្រមុះ-និងបំពង់ក/",
                  f"{base_url}/ជំងឺទឹកនោមផ្អែម/",
                  f"{base_url}/សុខភាពស្ត្រី/",
                  f"{base_url}/សុខភាពបុរស/",
                  f"{base_url}/ដំណេក/",
                  f"{base_url}/សុខភាពស្បែក/",
                  f"{base_url}/របបអាហារ/",
                  f"{base_url}/សុខភាពមនុស្សចាស់/",
                  f"{base_url}/សុខភាពផ្លូវភេទ/",
                  f"{base_url}/សុខភាពផ្លូវចិត្ត/",
                  f"{base_url}/ពពោះ/",
                  f"{base_url}/សុខភាពមាត់ធ្មេញ/",
                  f"{base_url}/ចិញ្ចឹមកូន/",
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
        articles = response.css("div.articles h3.title a::attr(href)").getall()

        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

            current_url = response.url
            next_page = self.get_next_page_url_with_param(current_url)
            if next_page:
                yield response.follow(next_page, callback=self.parse)

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
        item = ScrapyItem()
        item["category"] = response.css("div.mantine-Breadcrumbs-root a[label]::text").getall()
        item["title"] = response.css("h1.article-header::text").get()
        all_text = "".join(response.css("div.body-content p::text").getall())
        item["content"] = all_text
        item["url"] = result

        yield item
