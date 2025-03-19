"""Test Case For Popoluar website Cambodia"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.popular import PopularkhSpider
from url_khmer_scraping.jsonl_scraper.utils.pagination_handle import PaginationHandle

popularkh_spider = PopularkhSpider()
pagination_handle = PaginationHandle()

def test_parse_data_popularkh():
    """
    Test the parse_data method of PopularkhSpider.

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
        "category": "តារា",
        "title": "(វីដេអូ) ហេតុតែប្រុសស្អាត! ថេណា ប្តូរស្ទីលស្លៀកឈុតនេះ បង្ហោះលើ TikTok មួយភ្លែតសោះ មានអ្នក Like អ្នកសរសើរព្រាត",
        "content": (
            "ជាការពិតណាស់ តារាចម្រៀង Original Song លោក ថេណា "
            "មិនត្រឹមតែទទួលបានការគាំទ្រក្នុងនាមជាតារាចម្រៀងតែប៉ុណ្ណោះទេ តែតារាចម្រៀងរូបនេះ មានសន្ទុះខ្លាំងលើទីផ្សារពាណិជ្ជកម្ម ដោយលោកបានក្លាយទៅជា BA "
            "របស់ក្រុមហ៊ុនជាច្រើន។ងាកមកកាន់រូបសម្រស់ឯណោះវិញ លោក ថេណា ត្រូវបានចាត់ទុកជាតារាចម្រៀងប្រុសមានមន្តស្នេហ៍មួយរូប ដែលទទួលបានការស្រឡាញ់ពីអ្នកគាំទ្រ មិនថាប្រុស "
            "ឬស្រីនោះទេ។ ក្នុងនោះ រាល់ការបង្ហោះសារ ឬរូបភាពម្តងៗលើបណ្តាញសង្គមហ្វេសប៊ុក ឬ Tik Tok របស់លោក តារាចម្រៀងសំឡេងស្រទន់ ថេណា មានអ្នក Like និង ខមមិនព្រោងព្រាត។ជាក់ស្តែងមុននេះបន្តិច លោក ថេណា "
            "បានបង្ហោះវីដេអូមួយ ដែល Check in នៅឯស្រុកកំណើត នាទីរួមខេត្តកោះកុងមិនប៉ុន្មាននាទីផង មានអ្នកចូលទៅខមមិនរាប់រយទៅហើយ។ លើសពីនោះ អ្វីដែលកាន់តែចាប់អារម្មណ៍ គឺលោក ថេណា "
            "បានស្លៀកឈុតសម្លៀកបំពាក់ប្លែងជាងសព្វមួយដង ដោយលោកស្លៀកខោខ្មៅ ពាក់អាវក្រណាត់ខ្មៅដៃវែង ពាក់ស្បែកជើងខ្មៅ និង ស្ពាយកាបូបមនុស្សស្រី។វីដេអូនោះដែរ លោក ថេណា បានផ្អៀងផ្អងកាច់រាង "
            "បង្វិលខ្លួនមួយជុំដូចតារាម៉ូដែល កាន់តែធ្វើឱ្យអ្នកគាំទ្រទប់ចិត្តមិនជាប់ ស្រែកវ៉ាវ សរសើរថាមកម្តងនេះ ថេណា ឃ្យូដណាស់៕"
    )}

    article_url =  "https://www.popular.com.kh/entertainment/897578.html/"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(popularkh_spider.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url


def test_parse_popularkh():
    """
    Test the parse method of PopularkhSpider.

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
        - The number of article links (excluding the next page link) is 9.
        - The 10th link is the URL for the next page.
        - The next page URL matches the expected URL.
    """
    category_url = "https://www.popular.com.kh/category/fashion/"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = popularkh_spider.parse(category_response)

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
    assert links[10] == "https://www.popular.com.kh/category/fashion/page/2"
