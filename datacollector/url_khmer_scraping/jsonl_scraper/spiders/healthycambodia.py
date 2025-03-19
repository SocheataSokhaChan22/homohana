"""
Scrapy Spider for Healthy Cambodia

"""
import json
import scrapy
from ..items import ScrapyItem


class HealthyCambodiaSpider(scrapy.Spider):
    """
    A scrapy spider class inherited from the scrapy library.

    Attributes
    ----------
    name : str
        A string which defines the name for this spider.
    allowed_domains : list of str
        A list of strings containing domains that this spider is allowed to crawl.
    base_url : str
        The base URL of category of the website.
    ajax_url : str
        The URL for fetching article data.
    headers : dict
        Headers for the request.
    start_urls : list of str
        URLs where the spider will begin to crawl from.
    """
    name = "healthycambodia"
    allowed_domains = ["healthy-cambodia.com", "admin.healthy-cambodia.com"]
    base_url = "https://healthy-cambodia.com/categories"
    ajax_url = "https://admin.healthy-cambodia.com/items/article"
    headers = {
        "Origin": "https://healthy-cambodia.com",
        "Content-Type": "application/json; charset=utf-8",
        "Host": "admin.healthy-cambodia.com"
    }
    start_urls = [
            f"{base_url}/news",
            f"{base_url}/diseases",
            f"{base_url}/psychology",
            f"{base_url}/food",
            f"{base_url}/exercise",
            f"{base_url}/baby-care",
            f"{base_url}/business-idea",
            f"{base_url}/beauty",
            f"{base_url}/pr",
            ]

    def parse(self, response, **kwargs):
        """
        Parse the initial response to extract article links and handle AJAX pagination.

        Attributes:
        ------------
        form_data: dict
            The data sent in the AJAX request to load more articles.

        Parameters:
        ------------
        response: scrapy.http.Response
            The response object containing the initial page data.

        Yields:
        -------
        scrapy.FormRequest
            A FormRequest object that is sent to the AJAX URL to fetch more articles.
        """
        category_slug = response.url.split("/")[-1]
        page = 1

        form_data = {
            "limit": "8",
            "page": str(page),
            "sort": "-date_created",
            "filter[category][slug][_eq]": category_slug,
            "filter[status]": "published",
            "fields": "title,slug,category.name,description"
        }

        yield scrapy.FormRequest(
            url=self.ajax_url,
            headers=self.headers,
            method="GET",
            formdata=form_data,
            callback=self.parse_data,
            meta={"category_slug": category_slug, "page": page}
        )

    def parse_data(self, response):
        """
        Parse the JSON response to extract article details and handle pagination.
        It extracts relevant data such as the article title, category name, content, and URL.
        After that, it constructs a new request for the next page to continue scraping.

        Attributes:
        ------------
        data: json
            The JSON data extracted from the response.
        articles: dict
            A dictionary containing the article details.
        category_slug: str
            The slug of the category.
        page: int
            The current page number.
        form_data: dict
            The form data to be sent in the next request.
        next_page: int
            The page number for the next request.

        Yields:
        -------
        scrapy.FormRequest
            A FormRequest object that is sent to the AJAX URL to fetch more articles.
        """
        data = json.loads(response.text)
        articles = data.get("data", [])
        category_slug = response.meta["category_slug"]
        if articles:
            for article in articles:
                category = article.get("category", {}).get("name")
                url = "https://healthy-cambodia.com/article/" + article["slug"]
                yield response.follow(url, self.parse_article, cb_kwargs={"category": category})

            # Handle pagination
            page = response.meta["page"]
            next_page = page + 1

            form_data = {
                "limit": "8",
                "page": str(next_page),
                "sort": "-date_created",
                "filter[category][slug][_eq]": category_slug,
                "filter[status]": "published",
                "fields": "title,slug,category.name,description"
            }

            yield scrapy.FormRequest(
                url=self.ajax_url,
                headers=self.headers,
                method="GET",
                formdata=form_data,
                callback=self.parse_data,
                meta={"category_slug": category_slug, "page": next_page}
            )

    def parse_article(self, response, category):
        """
        This parsing article for Healthy Cambodia Website.
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
        item["category"] = category
        item["title"] = response.css(".article-title ::text").get()
        item["content"] = "".join(response.css("#article-body .article_body p *::text").getall())
        item["url"] = result

        yield item
