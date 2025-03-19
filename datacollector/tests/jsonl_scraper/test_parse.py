"""
Test Case for Parse Class and Parse Data Function

This module will test all spiders using the parse data function
from the Parser class.
"""
import pytest
import requests

from scrapy.http import HtmlResponse

# from jsonl_format import jsonl_formatter (If further testing is necessary)

from url_khmer_scraping.jsonl_scraper.spiders.parse import Parser

from url_khmer_scraping.jsonl_scraper.spiders.newsroom import NewsroomSpider

# Initialize the parser class and all spiders using the parser class
parser = Parser()
newsroom = NewsroomSpider()

# Set up URLs for parameterization
newsroom_url = "https://newsroomcambodia.com/news/2024/06/24/mr-hun-sen-appeal-to-use-cool-app/"


@pytest.mark.parametrize("spider, url", [(newsroom,newsroom_url)])

def test_parse_data_online(spider, url):
    """
    This function is used to test the parse data function.
    Parametrized for testing all spiders relying on this class.
    This test is conducted using live data from the website.
    Utilize data from the URL in real time rather than mock.

    Parameter
    ---------
    spider: class
        defined scrapy spider class
    url: str
        string for the URL of the article

    Attribute
    ---------
    response:
        live response from website by url
    html_response:
        html response generated from request
    result: generator obj
        stores the generator object yielded from the parse_data method
    article: dict
        stores the actual desired output
    """
    response = requests.get(url)
    html_response = HtmlResponse(url=response.url, body=response.text, encoding="utf-8")
    result = spider.parse_data(html_response)
    for article in result:
        assert article["title"] != ""  # article['content'] == jsonl_formatter.get_content(url)
        assert article["content"] != {}  # article['warc_headers']['warc-target-uri'] == url
        assert article["url"] != {}  # article['metadata'] == jsonl_formatter.get_metadata(jsonl_formatter.get_content(url))
