"""
Scrapy Spider for គេហទំព័រសុខភាព

Crawls the health.com.kh website for articles
"""
import json
import scrapy
from ..items import ScrapyItem


class HealthSpider(scrapy.Spider):
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
    ajas_url: str
        The URL of the AJAX request.
    base_url: str
        The base URL of category of the website.
    illness_url: str
        The URL of the illness category.
    start_urls: str
        URLs where the spider will begin to crawl from.
        The first pages downloaded will be those listed here.
        The subsequent request will be generated successively
        from data contained in the start URLs.
    """
    name = "health"
    allowed_domains = ["health.com.kh"]
    ajax_url = "https://www.health.com.kh/wp-admin/admin-ajax.php"
    base_url = "https://www.health.com.kh/archives/category"
    illness_url = f"{base_url}/illness"
    start_urls = [
        # illness category
        f"{illness_url}/lungdisease",
        f"{illness_url}/heart",
        f"{illness_url}/ជំងឺផ្លូវចិត្ត",
        f"{illness_url}/diabetes",
        f"{illness_url}/lungcancer",
        f"{illness_url}/std",
        f"{illness_url}/ជំងឺឆ្អឹងសន្លាក់",
        f"{illness_url}/breastcancer",
        f"{illness_url}/ជំងឺភ្នែក",
        f"{illness_url}/cancer",
        f"{illness_url}/highbloodpressure",
        f"{illness_url}/covid-19",
        f"{illness_url}/uteruscancer",
        f"{illness_url}/liver",
        f"{illness_url}/digestive",
        f"{illness_url}/stroke",
        f"{illness_url}/bladder",
        f"{illness_url}/lung",
        f"{illness_url}/viraldisease",
        f"{illness_url}/ជំងឺស្បែក",
        f"{illness_url}/ជំងឺត្រចៀក",
        f"{illness_url}/ជំងឺកុមារ",
        # Other Category
        f"{base_url}/dailynews",
        f"{base_url}/pamak",
        f"{base_url}/កុមារ",
        f"{base_url}/test",
        f"{base_url}/treatment",
        f"{base_url}/symptom",
        f"{base_url}/press-release",
        f"{base_url}/ឱសថ",
         ]

    def parse(self, response, **kwargs):
        """
        Parse the initial response to extract article links and handle AJAX pagination.
        If the page contains an "infinite-scroll" widget, it triggers a FormRequest
        to load more articles by simulating a "Load More" AJAX request.

        Attributes:
        ------------
        category_name: str
            The name of the category being scraped.
        articles: str
            A list of article links extracted from the page.
        widget_id: str
            The ID of the "infinite-scroll" widget.
        post_id: str
            The ID of the post.
        form_data: dict
            The data sent in the AJAX request to load more articles.
        meta: dict
            The meta data of the page.
        Yields: dict
            A dictionary with a single key "link", containing the URL of an article.
        Makes a FormRequest to:
            - Fetch more articles using AJAX if "infinite-scroll" is present on the page.
            - Passes the necessary parameters widget ID, post ID, and category name to the request.
        """
        # Extracts the last part of the URL as the category name
        category_name = response.url.split("/")[-1]
        articles = response.css("div.post-item h3.title a::attr(href)").getall()
        for article in articles:
            yield response.follow(article, self.parse_data)

        widget_id = response.css("a.infinite-scroll::attr(data-widget-id)").get()
        post_id = response.css("a.infinite-scroll::attr(data-post-id)").get()

        if widget_id and post_id:
            form_data = {
                "action": "rivax_get_load_more_posts",
                "widgetId": widget_id,
                "postId": post_id,
                "pageNumber": "2",
                "qVars[category_name]": category_name
            }
            meta = {
                "widget_id": widget_id,
                "post_id": post_id,
                "page_number": 2,
                "category_name": category_name
            }
            yield scrapy.FormRequest(
                url=self.ajax_url,
                formdata=form_data,
                callback=self.parse_data_ajax,
                meta=meta
            )

    def parse_data_ajax(self, response):
        """
        parse_data_ajax hanndles the AJAX response. This method processes the AJAX response,
        extracts article links from the HTML content. If more articles are available
        (i.e., no "no_more flag is set), it recursively sends another AJAX request to
        load additional articles.

        Attributes:
        ------------
        data: dict
            The data sent in the AJAX request to load more articles.
        meta: dict
            The meta data of the page.
        form_data: dict
            The data sent in the AJAX request to load more articles.
        no_more: bool
            A flag indicating whether there are more articles to load.
        Yields: dict
            A dictionary containing the link of each article extracted from the AJAX response.
            A request to fetch more articles via AJAX if more articles are available.
        """
        data = json.loads(response.text)
        html_content = data.get("data", "")
        if html_content:
            selector = scrapy.Selector(text=html_content)
            articles = selector.css("div.post-item h3.title a::attr(href)").getall()
            for article in articles:
                yield response.follow(article, self.parse_data)

            no_more = data.get("no_more", False)
            if not no_more:
                page_number = response.meta["page_number"] + 1
                form_data = {
                    "action": "rivax_get_load_more_posts",
                    "widgetId": response.meta["widget_id"],
                    "postId": response.meta["post_id"],
                    "pageNumber": str(page_number),
                    "qVars[category_name]": response.meta["category_name"]
                }
                meta = {
                    "widget_id": response.meta["widget_id"],
                    "post_id": response.meta["post_id"],
                    "page_number": page_number,
                    "category_name": response.meta["category_name"]
                }
                yield scrapy.FormRequest(
                    url=self.ajax_url,
                    formdata=form_data,
                    callback=self.parse_data_ajax,
                    meta=meta
                )

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

        if "archives/" in result:
            item = ScrapyItem()
            item["category"] = response.css("div.category span::text").get()
            item["title"] = response.css("div.single-hero-title h1.title::text").get()
            post_id = response.css("article::attr(id)").get()
            item["content"] = response.css(f"article[id='{post_id}'] *::text").getall()
            item["url"] = result

            yield item
