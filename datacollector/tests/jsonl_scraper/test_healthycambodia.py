"""Test Case For Healthy Cambodia"""
import requests
from scrapy.http import HtmlResponse, TextResponse, Request
from url_khmer_scraping.jsonl_scraper.spiders.healthycambodia import HealthyCambodiaSpider
import json

healthycambodia = HealthyCambodiaSpider()

def test_parse_healthycambodia():
    """
    Test the `parse` method of the HealthyCambodiaSpider.

    Attributes:
    ----------
    category_url (str):
        The URL of the news category to be tested.
    category (Response):
        The HTTP response object for the category URL.
    category_response (HtmlResponse):
        The response object to be passed to the spider's `parse` method.
    category_result (generator):
        The generator returned by the spider's `parse` method, yielding requests.
    """
    category_url = "https://healthy-cambodia.com/categories/news"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = healthycambodia.parse(category_response)

    """
    testing the parsing category 
    """
    form_request = next(category_result)
    assert form_request.meta["category_slug"] == "news"
    assert form_request.meta["page"] == 1
    assert form_request.method == "GET"


def test_parse_data_healthycambodia():
    """
    Test the `parse_data` method of HealthyCambodiaSpider.
    
    Attributes:
    ----------
    ajax_url (str):
        The URL for the AJAX request to fetch articles.
    category_slug (str):
        The slug for the news category being tested.
    form_data (dict):
        The query parameters for the AJAX request.
    ajax_response (Response):
        The HTTP response object from the AJAX request.
    ajax_json (dict):
        The JSON data parsed from the AJAX response.
    request (Request):
        The request object created for the AJAX URL.
    json_body (bytes):
        The JSON data encoded as bytes for the response.
    response (TextResponse):
        The response object to be passed to the spider's `parse_data` method.
    items_generator (generator):
        The generator returned by the spider's `parse_data` method.
    items_list (list):
        The list of articles extracted from the generator.
    """
    ajax_url = "https://admin.healthy-cambodia.com/items/article"
    category_slug = "news"
    
    form_data = {
        "limit": "8",
        "page": "1",
        "sort": "-date_created",
        "filter[category][slug][_eq]": category_slug,
        "filter[status]": "published",
        "fields": "title,slug,category.name,description"
    }

    # Make the GET request with query parameters
    ajax_response = requests.get(ajax_url, params=form_data)
    ajax_json = ajax_response.json()

    request = Request(url=ajax_url, meta={"category_slug": category_slug, "page": 1})
    json_body = json.dumps(ajax_json).encode("utf-8")

    response = TextResponse(url=ajax_url, body=json_body, request=request)

    items_generator = healthycambodia.parse_data(response)
    items_list = list(items_generator)

    assert len(items_list)-1 == 8
    assert items_list[8].url == "https://admin.healthy-cambodia.com/items/article?limit=8&page=2&sort=-date_created&filter%5Bcategory%5D%5Bslug%5D%5B_eq%5D=news&filter%5Bstatus%5D=published&fields=title%2Cslug%2Ccategory.name%2Cdescription"

def test_parse_article():
    """
    Test the parse_article method of HealthyCambodiaSpider()

    Attributes:
    -------------
    article_url (str):
        URL of the article to be tested.
    article_response (HtmlResponse):
        The response object for the article URL.
    article_result (list):
        Parsed data from the article page.
    expected_value (dict):
        Expected result of the parsed data. 

    Assertions:
        - The 'title' field of the parsed article is not empty.
        - The 'content' field of the parsed article is not empty.
        - The 'url' field of the parsed article is not empty.
    """
    expected_value = {
        "category": "សម្រស់",
        "title": "រយៈពេល៣ខែ ស្រកបាន 11.5kg មកព្រមជាមួយរូបរាងសាច់ដុំកង់ៗ",
        "content": (
            "រយៈពេល៣ខែ ស្រកបាន 11.5kg មកព្រមជាមួយរូបរាងសាច់ដុំកង់ៗបែបនេះ Boy Bakong ប្រាប់ថាមិននឹងស្មានថាមនុស្សដែលកំពូលខ្ជិលហាត់ប្រាណ ចូលចិត្តញ៉ាំច្រើនដូចជាគាត់ អាចមានរូបរាងបែបនេះបាន "
            "ជាការផ្លាស់ប្តូរធំបំផុតក្នុងជីវិត ចឹងយើងមកដឹងថាគាត់បានធ្វើអីខ្លះអាចទើបប្ដូររូបរាងទាំងស្រុងបែបនេះក្នុងរយៈពេលខ្លីបាន។ "
            "តាមការឱ្យដឹងពីសាមីខ្លួន លោកBoy Bakong ផ្ទាល់លោកបានឱ្យដឹងថា គីឡូដំបូងរបស់លោក  71.8kg អីលូវនេះសល់ត្រឹម 60.3kg តែប៉ុណ្ណោះ បន្ទាប់ពីចំណាយពេល៣ខែបផ្លាស់ប្តូរខ្លួនឯង។ គាត់ថានិយាយថា "
            "រូបរាងសាច់សុំ 6pack ដែលគាត់ទទួលបាននេះ សម្រាប់គាត់គឺពេញចិត្តបំផុត និងឡូយបំផុត ជាលើកទី១ក្នុងជីវិតរបស់គាត់ហើយ ក្នុងវ័យ៣៩ឆ្នាំ ដែលអាចមានរូបរាងបែបនេះ ។លោកបានលើកទឹកចិត្តថា "
            "បើគាត់ធ្វើបានហើយ គ្រប់គ្នាដឹងតែធ្វើបានដូចគ្នា ពីព្រោះគាត់ជាមនុស្សម្នាក់ដែលមិនខ្ជិលហាត់ប្រាណ មិនចូលចិត្តទេហាត់ cardio អីនឹង បើនិយាយពីរឿងញ៉ាំវិញ អាចនិយាយបានថា ញ៉ាំជាជិវីត "
            "ពីមុនសឹងតែថារស់ដើម្បីញ៉ាំតែម្ដង ជាមនុស្សម្នាក់ដែលញ៉ាំច្រើនហើយចូលចិត្តញ៉ាំណាស់។ ប៉ុន្តែដោយសារមានអាជីពជាតារាសម្ដែង "
            "ហើយអាយុក៏ច្រើនហើយដែរ ដើម្បីសុខភាព និងរក្សារូបរាងលោកក៏សម្រេចចិត្តជាលើកចុងក្រោយថានឹងតស៊ូទាល់តែបាន។ អ្វីដែលគាត់បានធ្វើ គឺកាត់ជាស្ករ កាត់ចិត្តពីនំកញ្ចប់ ដែលគាត់ធ្លាប់តែញ៉ាំរាល់យប់ កាត់ចិត្តពីពពួកគ្រឿង "
            "ញ៉ាំ ភ្លាម បុកល្ហុង និយាយទៅប្តូរចេញទាំងស្រុងតែម្ដង ទ្រាំកាត់ចិត្តឈប់ញ៉ាំអាហារដែលធ្លាប់ចូលចិត្តពីមុន មកជារបបអាហារដែលជំនួយសុខភាព និងសាច់ដុំវិញ "
            "ហើយកាត់បន្ថយការញ៉ាំមិនញ៉ាំច្រើនដូចមុន។ រឿងទី២ដែលធ្វើនោះ គឺហាត់ប្រាណដែលលោកទម្ងន់ និង cardio ១ថ្ងៃ១ម៉ោងកន្លះជាប្រចាំថ្ងៃ កន្លែងនេះគាត់និយាយថា មនុស្សខ្ជិលសឹងអី ឱ្យមកហាត់ប្រាណ "
            "ហត់ណាស់សឹងតែបោះបង់ម្ដងៗហើយ តែគាត់មានគ្រូជួយជម្រុញ ហើយក៏ព្យាយាមជម្រុញចិត្តខ្លួនឯងបន្ថែម។ បើសួគាត់ថា កំឡុងពេលនឹងពិបាកអត់ ពិតពិបាក ហត់ ហើយដំបូងមានអារម្មណ៍ថាធុញទៀត តែត្រូវតែតាំងចិត្ត "
            "ហើយជឿគាត់ទៅផ្ដល់ពេលវេលាឱ្យខ្លួនឯង ស៊ូទ្រាំធ្វើកុំបោះបង់ យើងនឹងអាចកែប្រែខ្លួនឯងបាន។ គាត់ក៏ប្រាប់ដែរ ថាអីលូវនេះគឺគាត់ពេញចិត្តនឹងរូបរាងខ្លួនឯងខ្លាំងណាស់ មានក្ដីសុខជាងមុន "
            "សំខាន់សុខភាពរបស់គាត់កាន់តែប្រសើរឡើង ល្អជាងមុនដាច់។ បន្ថែមពីនោះ គ្រូបង្វឹករបស់គាត់បានបញ្ជាក់ថា សង្ឃឹមថាលទ្ធផលមួយនេះនឹងក្លាយជាកម្លាំងចិត្តដល់បងប្អូនផ្សេងទៀត ឱ្យងាកមកមើលថែសុខភាព និងរូបរាងខ្លួន។ "
            "គោលដៅ + ការពិត + វិធីសាស្រ្ត + វិន័យ = លទ្ធផល។ ")
        }
    
    article_url = "https://healthy-cambodia.com/article/boy-bakong-"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(healthycambodia.parse_article(article_response, category="សម្រស់"))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url