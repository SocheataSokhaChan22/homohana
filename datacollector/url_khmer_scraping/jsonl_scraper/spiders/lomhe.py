"""
Scrapy Spider for lomhe.
Crawls the Khmer lomhe website for articles.
"""
import json
import scrapy
from ..items import ScrapyItem


class LomheSpider(scrapy.Spider):
    """
    A scrapy spider class inherited from the scrapy library.

    Attribute
    ----------
    name: : str
        A string which defines the name for this spider.
    allowed_domain: str
        list of strings containing domains that this
        spider is allowed to crawl.
    ajax_url : str
        The URL for making AJAX POST requests to fetch articles.
    base_url: The base URL of category of the website.
    start_urls: str
        URLs where the spider will begin to crawl from.
        The first pages downloaded will be those listed here.
    """
    name = "lomhe"
    allowed_domains = ["lomhe.com", "graph-kh.mediaload.co"]
    ajax_url = "https://graph-kh.mediaload.co/"
    base_url = "https://lomhe.com/category"
    start_urls = [f"{base_url}/food-travel-lets-eat/",
                  f"{base_url}/food-travel-lets-drink/",
                  f"{base_url}/food-travel-lets-visit/",
                  f"{base_url}/food-travel-lets-explore/",
                  ]

    def create_payload(self, category_slug, offset):  # pylint: disable=no-self-use
        """
        Creates the payload for AJAX requests to fetch articles.

        Parameters
        ----------
        category_slug : str
            The slug for the article category.
        offset : int
            The pagination offset value.
        Returns
        -------
        dict
            Payload for the AJAX POST request.
        """
        sha256 = "5d04e712e9b042e412d65511fa7dfa97ee1d4076e0ff0eb144dbb6f1f48e25f4"
        return {
            "operationName": "ArticleListPagination",
            "variables": {
                "pagination": {
                    "offset": offset,
                    "limit": 10
                },
                "filter": {
                    "siteId": 8,
                    "categoryId": 44,
                    "categorySlugSub": category_slug,
                    "categoryExceptIds": []
                }
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": sha256
                }
            }
        }

    def parse(self, response, **kwargs):
        """
        Parses the initial category page and sends a request to fetch articles.

        Parameters
        ----------
        response : scrapy.http.Response
            The response from the category page.
        """
        category_slug = response.url.rstrip("/").split('/')[-1]
        payload = self.create_payload(category_slug, offset=1)

        yield scrapy.Request(
            url=self.ajax_url,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=json.dumps(payload),
            callback=self.parse_articles,
            meta={"category_slug": category_slug, "offset": 1}
        )

    def parse_articles(self, response):
        """
        Parses the AJAX response and yields article details.

        Parameters
        ----------
        response : scrapy.http.Response
            The response from the AJAX request with article data.
        """
        data = json.loads(response.text)
        articles = data.get("data", {}).get("articleList", {}).get("listData", [])
        if articles:
            for article in articles:
                url = article.get("id")
                article_url = "https://lomhe.com/article/" + str(url)
                yield response.follow(article_url, self.parse_data)

            offset = response.meta["offset"] + 1
            category_slug = response.meta["category_slug"]
            payload = self.create_payload(category_slug, offset)

            yield scrapy.Request(
                url=self.ajax_url,
                method="POST",
                headers={"Content-Type": "application/json"},
                body=json.dumps(payload),
                callback=self.parse_articles,
                meta={"category_slug": category_slug, "offset": offset}
            )

    def parse_data(self, response):
        """
        Parses the article page and extracts relevant data.

        Parameters
        ----------
        response : scrapy.http.Response
            The response from the article page.
        """
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")
        item = ScrapyItem()
        item["category"] = response.css(".article-summary-category ::text").get()
        item["title"] = response.css(".article-tracker .grid-article-title::text").get()
        content = ".article-summary-title-sub ::text, .grid-article-content ::text"
        item["content"] = "".join(response.css(content).getall())
        item["url"] = result

        yield item
