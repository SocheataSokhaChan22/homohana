"""
Scrapy Spider for Ohh Cambodia
Crawls the Ohh Cambodia website for articles
"""
import json
import scrapy
from ..items import ScrapyItem
from ..utils.pagination_handle import PaginationHandle


class OhhcambodiaSpider(scrapy.Spider, PaginationHandle):
    """
    A scrapy spider class inherited from the scrapy library.

    Attribute
    ----------
    name: : str
        A string which defines the name for this spider.
    start_urls: str
        URLs where the spider will begin to crawl from.
    allowed_domain: str
        An optional list of strings containing domains that this
        spider is allowed to crawl.
    ajax_url: str
        The URL for the AJAX request to fetch articles.
    custom_settings: dict
        configuration we can set up for an individual spider to alter the default settings.
    """
    name = "ohhcambodia"
    custom_settings = {
        "USER_AGENT": (
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)"
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 "
            "Mobile Safari/537.36"
        )
    }
    allowed_domains = ["ohhcambodia.com"]
    base_url = "https://ohhcambodia.com"
    ajax_url = "https://ohhcambodia.com/jm-ajax/get_listings/"
    start_urls = [f"{base_url}/blog/",
                  f"{base_url}/listings/"]

    def parse(self, response, **kwargs):
        """
        Process the response from the initial request and handle pagination.

        This method processes the downloaded responses, extracts article links from
        the blog or listings page, and handles pagination. Depending on the category
        (blog or listings), it either extracts articles or sends AJAX requests for listings.
        If pagination is present, it follows the next page link.

        Attributes
        ----------
        category_name : list
            list of URL segments used to identify if current page is a 'blog' or 'listings' page.
        articles : list
            A list of article URLs extracted from the 'blog' page.
        form_data : dict
            A dictionary containing data for the AJAX POST request when parsing the 'listings' page.
        next_page : str
            URL of the next page to follow if pagination exists for the 'blog' page.
        current_page : str
            The URL of the current page being processed.
        Yields
        ------
        scrapy.Request
            Requests to follow article links, fetch the next page, or load more listings via AJAX.
        """
        category_name = response.url.rstrip("/").split("/")
        if "blog" in category_name:
            articles = response.css(".entry-title a ::attr(href)").getall()
            if articles:
                for article in articles:
                    yield response.follow(article, self.parse_data, cb_kwargs={"category": None})

                current_page = response.url
                next_page = self.get_next_page_url(current_page)
                if next_page:
                    yield response.follow(next_page, self.parse)
        elif "listings" in category_name:
            form_data = {
                "per_page": "50",
                "orderby": "featured",
                "featured_first": "false",
                "order": "DESC",
                "page": "1"
            }

            yield scrapy.FormRequest(
                url=self.ajax_url,
                formdata=form_data,
                callback=self.parse_data_ajax,
                meta={"page_number": 1}
            )

    def parse_data_ajax(self, response):
        """
        This method processes the AJAX response, extracts article links from
        dynamically loaded HTML content (received as part of the AJAX response),
        and recursively sends additional AJAX requests if more articles are available.

        Attributes
        ----------
        data : dict
            The parsed JSON response data received from the AJAX request, containing
            the HTML content with listings.
        selector : scrapy.Selector
            A Selector object created from the extracted HTML content to parse the listings.
        listings : list
            A list of job elements extracted from the HTML content using CSS selectors.
        page_number : int
            The current page number being processed, which is incremented for the next AJAX request.
        form_data : dict
            The data dictionary used to send the AJAX POST request, including
            the page number and other parameters.

        Yields
        ------
        scrapy.Request
            Requests to follow article links extracted from the current AJAX response,
            or a new AJAX request to load more listings if available.
        """
        data = json.loads(response.text)
        if data and data['found_jobs']:
            listings = data.get('html', '')
            selector = scrapy.Selector(text=listings)
            listings = selector.css("div.job-grid-style")
            for listing in listings:
                article = listing.css("h3.listing-title a::attr(href)").get()
                category = listing.css("::attr(data-categories)").get()
                yield response.follow(article, self.parse_data, cb_kwargs={"category": category})
            # Load Next Page
            page_number = response.meta["page_number"] + 1
            form_data = {
                "per_page": "50",
                "orderby": "featured",
                "featured_first": "false",
                "order": "DESC",
                "page": str(page_number)
            }
            yield scrapy.FormRequest(
                url=self.ajax_url,
                formdata=form_data,
                callback=self.parse_data_ajax,
                meta={"page_number": page_number}
            )

    def parse_data(self, response, category):
        """
        This method processes the response from the article page or listings
        and extracts relevant information such as category, title, content,
        and URL.

        Parameters
        ----------
        category : str
            The category of the article passed via callback, used when processing listings.
        Yields
        ------
        ScrapyItem
            An item containing the extracted information (title, content, category, and URL).
        """
        item = ScrapyItem()
        result = response.url
        self.logger.info(f"A response from {response.url} just arrived!")

        if "listings/" in result:
            item["category"] = category
            item["title"] = response.css("h1.entry-title ::text").get()
            content = response.css(".entry-content .job_description ::text").getall()
            item["content"] = "".join(content)
            item["url"] = result

        else:
            item["category"] = ",".join(response.css(".categories a::text").getall())
            item["title"] = response.css(".info .entry-title::text").get()
            item["content"] = "".join(response.css(".entry-description *::text").getall())
            item["url"] = result

        yield item
