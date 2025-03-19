"""
Scrapy Spider for Khmer Food Recipes
Crawls the khmerfoodrecipes website for articles.
"""
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class KhmerfoodrecipesSpider(scrapy.Spider, PaginationHandle):
    """
    A Scrapy spider class for scraping the Khmer Food Recipes blog.
    Inherits from both Scrapy's Spider and PaginationHandle utility class.

    Attributes
    ----------
    name : str
        The name of the spider.
    allowed_domains : list
        A list of domains that this spider is allowed to crawl.
    start_urls : list
        The initial URLs where the spider starts crawling.
    """

    name = "khmerfoodrecipes"
    allowed_domains = ["khmerfoodrecipes.blogspot.com"]
    start_urls = ["https://khmerfoodrecipes.blogspot.com"]

    def parse(self, response, **kwargs):
        """
        Parses the initial response and retrieves category URLs for articles.

        This method fetches all available categories from the page and constructs URLs
        with pagination to scrape more articles from each category.

        Parameters
        ----------
        response : scrapy.http.Response
            The response object containing the HTML page to parse.
        """
        categories = response.css(".list-label-widget-content li a[dir='ltr']::attr(href)").getall()
        items = response.css(".list-label-widget-content li span[dir='ltr']::text").getall()

        if categories and items:
            for category, item in zip(categories, items):
                # Calculate max-results based on the number of articles in the category
                max_results = int(item.strip("()")) + 4
                category_url = f"{category}?&max-results={max_results}"
                yield response.follow(category_url, self.parse_articles)

    def parse_articles(self, response):
        """
        Extracts article URLs from the category page and follows each one.

        Attributes
        ----------
        articles: list of str
            A list of article URLs to follow.
        """
        articles = response.css(".entry-title a::attr(href)").getall()
        if articles:
            for article in articles:
                yield response.follow(article, self.parse_data)

    def parse_data(self, response):
        """
        Parses the article data and extracts the title, content, category, and URL.

        This method processes the response for an individual article and extracts
        relevant information such as the title, content, category, and URL.

        Yields
        ------
        ScrapyItem
            An item containing the extracted data from the article.
        """
        item = ScrapyItem()

        # Extract article metadata
        item["category"] = ",".join(response.css(".label-head ::text").getall())
        item["title"] = response.css("h1.entry-title ::text").get()
        item["content"] = "".join(response.css(".entry-content ::text").getall())
        item["url"] = response.url  # Store the article's URL

        self.logger.info(f"Scraped article from {response.url}")
        yield item
