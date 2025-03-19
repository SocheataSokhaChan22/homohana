"""Test Case For Biz Cambodia News"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.thehrdaily import ThehrdailySpider
from url_khmer_scraping.jsonl_scraper.utils.pagination_handle import PaginationHandle

thehrdaily_spider = ThehrdailySpider()
pagination_handle = PaginationHandle()

def test_parse_data_thehrdaily():
    """
    Test the parse_data method of `BizcambodiaSpider`.

    Attributes:
    -------------
    article_url (str):
        URL of the article to be tested.
    article_response (HtmlResponse):
        The response object for the article URL.
    article_result (list):
        Parsed data from the article page.
    expected_value: dict
        Expected result of the parsed data.

    Assertions:
        - The 'title' field of the parsed article is not empty.
        - The 'content' field of the parsed article is not empty.
        - The 'url' field of the parsed article is not empty.
    """
    expected_value = {
        "category": "ការគ្រប់គ្រង និងដឹកនាំ,ធនធានមនុស្ស",
        "title": "មនុស្សជំនាន់ Z កំពុងកាន់កាប់បន្ត…",
        "content": (
            "មនុស្សជំនាន់ Z កំពុងកាន់កាប់បន្ត។ នៅក្នុងពិភពអ្នកមាន មានមនុស្សយ៉ាងហោចណាស់ ២៥០ លាននាក់ "
            "កើតនៅចន្លោះឆ្នាំ១៩៩៧ ដល់ ឆ្នាំ២០១២។ ប្រហែលពាក់កណ្តាល កំពុងមានការងារធ្វើ។ "
            "នៅកន្លែងធ្វើការជាមធ្យមរបស់អាម៉េរិក ចំនួនមនុស្សជំនាន់ Z (ចួនកាលត្រូវបានគេស្គាល់ថាជា “Zoomers”) ដែលធ្វើការពេញម៉ោង គឺហៀបនឹងលើសចំនួនមនុស្សកើតសម័យសង្គ្រាម (Baby-boomers) ធ្វើការពេញម៉ោង ដែលកើតពីឆ្នាំ១៩៤៥ ដល់ ឆ្នាំ១៩៦៤ ដែលអាជីពរបស់ពួកគេ គឺរំកិលចុះក្រោម (សូមរូបភាពខាងក្រោម) ។ អាម៉េរិក "
            "ឥឡូវនេះមានប្រធាននាយកប្រតិបត្តិ Zoomer ជាង ៦,០០០នាក់ និងអ្នកនយោបាយ Zoomer ១,០០០នាក់។ នៅពេលដែលមនុស្សជំនាន់ Z កាន់តែមានឥទ្ធិពល ក្រុមហ៊ុន រដ្ឋាភិបាល "
            "និងអ្នកវិនិយោគត្រូវយល់អំពីវា។ប្រភព៖ The Economistអត្ថបទទាក់ទងរបាយការណ៍ថ្នាក់ជាតិ ស្ដីពីលទ្ធផលចុងក្រោយនៃជំរឿនសេដ្ឋកិច្ច នៅព្រះរាជាណាចក្រកម្ពុជា ឆ្នាំ២០២២ (ខែសីហា ឆ្នាំ២០២៣) "),
    }

    article_url = "https://www.thehrdaily.com/hr/page=123/មនុស្សជំនាន់-z-កំពុងកាន់/"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(thehrdaily_spider.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == "https://www.thehrdaily.com/hr/page=123/%E1%9E%98%E1%9E%93%E1%9E%BB%E1%9E%9F%E1%9F%92%E1%9E%9F%E1%9E%87%E1%9F%86%E1%9E%93%E1%9E%B6%E1%9E%93%E1%9F%8B-z-%E1%9E%80%E1%9F%86%E1%9E%96%E1%9E%BB%E1%9E%84%E1%9E%80%E1%9E%B6%E1%9E%93%E1%9F%8B/"

def test_parse_thehrdaily():
    """
    Test the parse method of `BizcambodiaSpider`.

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
    next_page (list):
        URL segments for constructing the next page URL.
    next_page_url (str):
        Constructed URL for the next page.

    Assertions:
        - The number of article links (excluding the next page link) is 20.
        - The 10th link is the URL for the next page.
        - The next page URL matches the expected URL.
    """

    category_url = "https://www.thehrdaily.com/management-and-leadership/page/24/"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = thehrdaily_spider.parse(category_response)

    """
    testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    
    """
    Test for pagination
    """
    next_page_url = pagination_handle.get_next_page_url(category_response.url)

    assert len(links) - 1 == 20
    assert links[20] == next_page_url
    assert links[20] == "https://www.thehrdaily.com/management-and-leadership/page/25"
