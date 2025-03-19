"""
Scrapy Spider for អង្គភាពសារព័ត៌មាន SBM

Crawls the SBM News website for articles
"""
import json
import scrapy
from ..items import ScrapyItem


class SBMSpider(scrapy.Spider):
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
    start_urls : list of str
        URLs where the spider will begin to crawl from.
    """
    name = "sbmnews"
    allowed_domains = ["sbm.news"]
    base_url = "https://sbm.news/categories/"
    ajax_url = "https://sbm.news/api/articles"
    start_urls = [f"{base_url}/hot/articles",
                  f"{base_url}/5fa83b9aabe3fdc2522f6c25/articles",  # ជាតិ
                  f"{base_url}/5fa83ba6abe3fdc2522f6c26/articles",  # អន្តរជាតិ
                  f"{base_url}/5fa83bb0abe3fdc2522f6c27/articles",  # នយោបាយ
                  f"{base_url}/5fa83be8abe3fdc2522f6c28/articles",  # សេដ្ឋកិច្ច
                  f"{base_url}/5fa83c51abe3fdc2522f6c29/articles",  # សន្តិសុខសង្គម
                  f"{base_url}/5fa83c5aabe3fdc2522f6c2a/articles",  # កម្សាន្ត
                  f"{base_url}/5fa83c64abe3fdc2522f6c2b/articles",  # កីឡា
                  f"{base_url}/5fa83c72abe3fdc2522f6c2c/articles",  # បច្ចេកវិទ្យា
                  f"{base_url}/5fa83c7eabe3fdc2522f6c2d/articles",  # សុខភាព
                  f"{base_url}/5ff801366421e7773b574a8b/articles",  # ចំណេះដឹង
                  f"{base_url}/6381a8c2b65e2b387f484a56/articles",  # ទុរគតជន
                  f"{base_url}/662678690168987bbf9af5c5/articles",  # កសិកម្ម
                  f"{base_url}/6626788d0168987bbf9af64a/articles",  # ទេសចរណ៏
                  f"{base_url}/66d1a14a37ec622bfdb644a9/articles",  # សង្គម
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
        category_id = response.url.split("/")[-2]

        form_data = {
            "page": "1",
            "categoryId": category_id,
            "locale": "km",
        }

        yield scrapy.FormRequest(
            url=self.ajax_url,
            method="GET",
            formdata=form_data,
            callback=self.parse_data,
            meta={"category_id": category_id, "page": 1}
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
        category_id: str
            The id of the category.
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
        articles = data.get("docs", [])
        category_id = response.meta["category_id"]
        if articles:
            for article in articles:
                item = ScrapyItem()
                item["category"] = ", ".join(article.get("categoryNames"))
                item["title"] = article["title"]
                item["content"] = article["content"]
                item["url"] = "https://sbm.news/articles/" + article["_id"]
                yield item

            # Handle pagination
            page = response.meta["page"]
            next_page = page + 1

            form_data = {
                "page": str(next_page),
                "categoryId": category_id,
                "locale": "km",
            }

            yield scrapy.FormRequest(
                url=self.ajax_url,
                method="GET",
                formdata=form_data,
                callback=self.parse_data,
                meta={"category_id": category_id, "page": next_page}
            )
