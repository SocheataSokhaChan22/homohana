"""Test Case For KhmerPlaces"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.khmerplace import KhmerPlacespSpider
from url_khmer_scraping.jsonl_scraper.utils.pagination_handle import PaginationHandle

khmerplaces = KhmerPlacespSpider()
pagination_handle = PaginationHandle()

def test_parse_data_khmerplaces():
    """
    This function is used to test the parse data method of KhmerPlacespSpider.
    This checks to see if the filtering works correctly.
    This test is conducted using live data from the website.

    Note: The filtering mainly focuses on the URL.

    Attribute
    ---------
    article_response:
        live response generated from article url
    category:
        live response generated from category url
    article_result:
        list of article urls generated from article response
    article: dict
        desired output (should be parsed)
    expected_value: dict
        Expected result of the parsed data.
    """
    expected_value = {
        "category": "កន្លែងញុំាអី, ចែវ-ជិះទូក, ភោជនីយដ្ឋាន, កន្លែងដើរលេង, ស្ទូចត្រី",
        "title": "បឹងឈូកថ្មី - Boeung Chhouk Thmey",
        "content": "បឹងឈូកថ្មី គឺជាកន្លែងដើរលេងមួយកន្លែងនៅជិតៗក្រុង ដែលមានចម្ងាយប្រមាណ១៥គីឡូម៉ែត្រពីវត្តភ្នំ ធ្វើដំណើរប្រហែល៤០នាទី។នៅទីនេះ មានដូចជា៖បឹងឈូកថ្មីនេះ ស្ថិតនៅភូមិចំពុះក្អែក សង្កាត់ព្រែកថ្មី ខណ្ឌច្បារអំពៅ រាជធានីភ្នំពេញ។ ពត៌មានទំនាក់ទំនង៖ ",
    }


    article_url = "https://www.khmerplaces.com/km/posts/boeung-chhouk-thmey"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")
    article = next(khmerplaces.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_khmerplaces():
    """
    Test of `parse` method of the khmerplaces spider.
    
    This test checks the following:
    - The title of the article is not empty.
    - The content of the article is not an empty dictionary.
    - The URL of the article is not an empty dictionary.

    Attributes:
    ----------
    category_url (str):
        The URL of the category page to be tested.
    category (Response):
        The HTTP response object for the category URL.
    category_response (HtmlResponse):
        The response object to be passed to the spider's `parse` method.
    category_result (list):
        The result returned by the spider's `parse` method.
    links (list):
        A list of URLs extracted from the category page.
    next_page (str):
        The URL of the next page after pagination.
    """
    category_url = "https://www.khmerplaces.com/km/categories/trip"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = khmerplaces.parse(category_response)

    """
    testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    
    """
    Test for pagination
    """
    next_page = category_response.css("div.page-pagination-2 a[rel='next']::attr(href)").get()

    assert len(links) - 1 == 16
    assert links[16] == next_page
    assert links[16] == "https://www.khmerplaces.com/km/categories/trip?page=2"
