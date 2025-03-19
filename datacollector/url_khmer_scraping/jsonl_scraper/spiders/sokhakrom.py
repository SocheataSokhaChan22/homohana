"""
Scrapy Spider for សុខក្រម Website Cambodia.
Crawls the sokhakrom website for articles.
"""
import json
import scrapy
from ..items import ScrapyItem


class SokhakromSpider(scrapy.Spider):
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
    start_urls: str
        URLs where the spider will begin to crawl from.
        The first pages downloaded will be those listed here.
        The subsequent request will be generated successively
        from data contained in the start URLs.
    """
    name = "sokhakrom"
    allowed_domains = ["sokhakrom.com"]
    base_url = "https://sokhakrom.com/kh"
    start_urls = [f"{base_url}/healthtip/list/data/all",
                  f"{base_url}/plant/list/data",
                  f"{base_url}/news/list/data"
                  ]

    def parse(self, response, **kwargs):
        form_data = {
            "page": "1",
            "search": "",
            "sort": "nto",
        }

        yield scrapy.FormRequest(
            url=response.url,
            method="GET",
            formdata=form_data,
            callback=self.parse_data_ajax,
            meta={"page": 1}
        )

    def parse_data_ajax(self, response):
        """
        Parse the JSON response to extract article details and handle pagination.
        It retrieves article data from the response, generates a follow-up request
        for each article's detail page, and continues pagination by constructing
        a new request for the next page.

        Parameters
        ----------
        response : scrapy.http.Response
            The HTTP response object that contains the JSON data.
        Attributes (local variables)
        ----------------------------
        data : dict
            The parsed JSON data from the response.
        articles : list
            A list of dictionaries, each containing details of an article.
        category : str
            The category name extracted from the URL for constructing the article URLs.
        page : int
            The current page number, extracted from the response metadata.
        next_page : int
            The next page number for pagination.
        form_data : dict
            The form data sent with the next pagination request to fetch more articles.

        Yields
        ------
        scrapy.http.Request or scrapy.FormRequest
            Either a request to follow the article's detail page or a FormRequest
            for the next page of the articles (pagination).
        """
        data = json.loads(response.text)
        articles = data['data']['data']
        category = response.url.rstrip("/").split("/")[4]
        if articles:
            for article in articles:
                url = self.base_url + f"/{category}/detail/" + str(article["id"])
                yield response.follow(url, self.parse_data, cb_kwargs={"category": category})

            # Handle pagination
            page = response.meta["page"]
            next_page = page + 1

            form_data = {
                "page": str(next_page),
                "search": "",
                "sort": "nto"
            }

            yield scrapy.FormRequest(
                url=response.url,
                method="GET",
                formdata=form_data,
                callback=self.parse_data_ajax,
                meta={"page": next_page}
            )

    def parse_data(self, response, category):
        """
        Parse the article detail page to extract information
        such as title, content, and URL.

        Parameters
        ----------
        response : scrapy.http.Response
            The HTTP response object that contains the HTML page of the article.
        category : str
            The category of the article, passed as a keyword argument.
        Yields
        ------
        ScrapyItem
            A Scrapy item containing the article's category, title, content, and URL.
        """
        self.logger.info(f"A response from {response.url} just arrived!")
        item = ScrapyItem()
        item["category"] = category
        item["title"] = response.css(".col-md-8 h3 ::text").get()
        item["content"] = "".join(response.css(".col-md-8 ::text").getall())
        item["url"] = response.url

        yield item
