"""Test Case For AMS Economy Website Cambodia"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.amseconomy import AMSEconomySpider
from url_khmer_scraping.jsonl_scraper.utils.pagination_handle import PaginationHandle

amseconomy_spider = AMSEconomySpider()
pagination_handle = PaginationHandle()

def test_parse_data_amseconomy():
    """
    Test the parse_data method of AMSEconomySpider.

    Attributes:
    -------------
    article_url (str):
        URL of the article to be tested.
    article_response (HtmlResponse):
        The response object for the article URL.
    article_result (list):
        Parsed data from the article page.
    expected_value (dic):
        Expected result of the parsed data.

    Assertions:
        - The 'title' field of the parsed article is not empty.
        - The 'content' field of the parsed article is not empty.
        - The 'url' field of the parsed article is not empty.
    """
    expected_value = {
        "category": "ព្រឹត្តិការណ៍,អត្ថបទពាណិជ្ជកម្ម",
        "title": "បញ្ជីរាយនាមសប្បុរសជនបរិច្ចាគសម្រាប់ប្រើប្រាស់និងគាំទ្រក្នុងសកម្មភាពរៀបចំព្រឹត្តិការណ៍​ Gumball3000 នៅកម្ពុជា​",
        "content":("(គិតត្រឹមថ្ងៃទី ០៣​ កញ្ញា​ ឆ្នាំ២០២៤)ក្រុមហ៊ុន ជីប ម៉ុង ក្នុងនាមជាដៃគូសហការផ្ដាច់មុខរបស់ GUMBALL3000 ក្នុង"
                   "ការរៀបចំព្រឹត្តិការណ៍នេះនៅកម្ពុជាដែលមានការគាំទ្រពី ក្រសួងទេសចរណ៍ និងស្ថាប័នពាក់ព័ន្ធនានា សូមថ្លែងអំណរគុណ"
                   "យ៉ាងជ្រាវជ្រៅដល់សប្បុរសជនដែលបានបរិច្ចាគសម្រាប់ប្រើប្រាស់ និងគាំទ្រក្នុងសកម្មភាពរៀបចំព្រឹត្តិការណ៍ "
                   "GUMBALL3000 នៅកម្ពុជា ដែលធ្វើឡើងនៅខែកញ្ញាខាងមុខនេះសម្រាប់គ្រប់ស្ថាប័នដែលមានបំណងចង់ចូលរួមជា"
                   "ចំណែកឧបត្តម្ភក្នុងព្រឹត្តិការណ៍ដ៍ធំប្រចាំឆ្នាំមួយនេះ លោកអ្នកអាចទំនាក់ទំនងមកក្រុមការងារដើម្បីទទួលនូវពត៍មាន"
                   "បន្ថែម**សម្រាប់ព័ត៌មានបន្ថែមអាចទាក់ទងមកផេក Rev Up Cambodia ផ្ទាល់ឬតាមលេខទូរស័ព្ទ : +855(0)67 734 734 / 60 671 123"), 
    }


    article_url = "https://economy.ams.com.kh/pr/news/list-of-donors-for-use-and-support-in-gumball3000-events-in-cambodia"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(amseconomy_spider.parse_data(article_response))
    assert expected_value["category"] in article["category"] 
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_amseconomy():
    """
    Test the parse method of AMSEconomySpider.

    Attributes:
    ------------
    category_url (str): 
        URL of the category page to be tested.
    category_response (HtmlResponse):
        The response object for the category URL.
    category_result (list):
        Parsed data from the category page.
    links (list):
        List of article links extracted from the category page.
    next_page_url (str):
        Constructed URL for the next page.
    Assertions:
        - The number of article links (excluding the next page link) is 10.
        - The 10th link is the URL for the next page.
        - The next page URL matches the expected URL.
    """

    category_url = "https://economy.ams.com.kh/category/all-news/news-realestate/"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = amseconomy_spider.parse(category_response)

    """
    Testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    
    """
    Test for pagination
    """
    next_page_url = pagination_handle.get_next_page_url(category_response.url)

    assert len(links) - 1 == 10
    assert links[10] == next_page_url
    assert links[10] == "https://economy.ams.com.kh/category/all-news/news-realestate/page/2"
