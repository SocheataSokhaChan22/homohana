"""Test Case For Lomhe website"""
import requests
from scrapy.http import HtmlResponse, Request, TextResponse
from url_khmer_scraping.jsonl_scraper.spiders.lomhe import LomheSpider
import json

lomhe_spider = LomheSpider()

def test_create_payload():
    """
    Test the `create_payload` method of the `LomheSpider` class.

    This test verifies that the payload created by the `create_payload` method
    matches the expected payload format for a given category slug and offset.

    Attributes:
    ----------
    category_slug (str):
        The slug of the category to be used in the payload.
    offset (int):
        The pagination offset to be used in the payload.
    payload (dict):
        The payload created by the `create_payload` method.
    expected_payload (dict):
        The expected payload for comparison.
    """

    category_slug = "food-travel-lets-eat"
    offset = 2
    payload = lomhe_spider.create_payload(category_slug, offset)

    expected_payload = {
        "operationName": "ArticleListPagination",
        "variables": {
            "pagination": {
                "offset": offset,
                "limit": 10
            },
            "filter": {
                "siteId": 8,
                "categoryId": 44,
                "categorySlugSub": category_slug,
                "categoryExceptIds": []
            }
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "5d04e712e9b042e412d65511fa7dfa97ee1d4076e0ff0eb144dbb6f1f48e25f4"
            }
        }
    }

    assert payload == expected_payload

def test_parse_lomhe():
    """
    Test the `parse` method of the `LomheSpider` class.

    This test performs the following checks:
    - Extracts all article URLs from the category page.
    - Tests the pagination by verifying that the last URL corresponds to the next page.
    - Ensures that the generated next page URL is correct.

    Attributes:
    ----------
    category_url (str):
        The URL of the category page to be tested.
    category (Response):
        The HTTP response object for the category URL.
    category_response (HtmlResponse):
        The response object to be passed to the spider's `parse` method.
    items (list):
        The list of results returned by the spider's `parse` method.
    item (dict):
        The first item in the list of results.
    """

    category_url = "https://lomhe.com/category/food-travel-lets-visit"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    items = list(lomhe_spider.parse(category_response))
    item = items[0]
    assert len(items) == 1
    assert item.url == "https://graph-kh.mediaload.co/"
    assert item.headers != ""
    assert item.meta["category_slug"] == "food-travel-lets-visit"
    assert item.meta["offset"] == 1

def test_parse_articles_lomhe():
    """
    Test the `parse_articles` method of the `LomheSpider` class.

    This test verifies that the articles are parsed correctly from the AJAX response.
    - Ensures that the number of items returned matches the expected limit.
    - Checks the attributes of the last item to confirm correct pagination.

    Attributes:
    ----------
    category_slug (str):
        The slug of the category for which the articles are being fetched.
    offset (int):
        The pagination offset for the AJAX request.
    meta (dict):
        Metadata including category slug and offset.
    payload (dict):
        The payload used in the AJAX request.
    ajax_response (Response):
        The HTTP response object for the AJAX request.
    json_body (bytes):
        The JSON response body encoded in UTF-8.
    request (Request):
        The request object to be used for creating a TextResponse.
    response (TextResponse):
        The response object to be passed to the spider's `parse_articles` method.
    items_list (list):
        The list of results returned by the spider's `parse_articles` method.
    """

    category_slug = "food-travel-lets-eat"
    offset = 2
    meta = {'category_slug': category_slug, 'offset': offset}
    payload = lomhe_spider.create_payload(category_slug, offset)
    
    ajax_response = requests.post(
        lomhe_spider.ajax_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )

    ajax_json = ajax_response.json()
    json_body = json.dumps(ajax_json).encode('utf-8')

    request = Request(url=lomhe_spider.ajax_url, meta=meta)
    response = TextResponse(url=lomhe_spider.ajax_url, body=json_body, request=request)

    items_generator = lomhe_spider.parse_articles(response)

    items_list = list(items_generator)
    assert len(items_list)-1 == 10
    assert items_list[-1].url == "https://graph-kh.mediaload.co/"
    assert items_list[-1].headers != ""
    assert items_list[-1].meta["category_slug"] == category_slug
    assert items_list[-1].meta["offset"] == 3

def test_parse_data_lomhe():
    """
    Test the `parse_data` method of the `LomheSpider` class.

    This test verifies the data extraction from an article page:
    - Ensures that the category of the article is not empty.
    - Checks that the title of the article is not empty.
    - Validates that the content of the article is not an empty dictionary.
    - Confirms that the URL of the article is correctly extracted.

    Attributes:
    ----------
    article_url (str):
        The URL of the article to be tested.
    article (Response):
        The HTTP response object for the article URL.
    article_response (HtmlResponse):
        The response object to be passed to the spider's `parse_data` method.
    article_result (list):
        The list of results returned by the spider's `parse_data` method.
    expected_value (dict):
        Expected result of the parsed data.
    """
    expected_value = {
        "category": "ភេសជ្ជះ",
        "title": "ចង់ញុំាទឹកកកឈូសទេ​ រៀនធ្វើខ្លួនឯង ចង់ដាក់លាយជាមួយផ្លែឈើក៏បាន",
        "content": ("ទឹកកកឈូសសម័យឥឡូវទំនើបណាស់ ឃើញគេលក់នៅតាមហាងមានច្រើនរសជាតិតែថ្លៃដែល មានតែកែច្នៃខ្លួនឯង "
                    "ដាក់ផ្លែឈើ ដាក់ទឹកសេរ៉ូ ទើបចំនេញលុយ។កម្សាន្ត៖ ទឹកកកឈូសជាបង្អែមដែលល្បីល្បាញជាយូរមកហើយ\nប៉ុន្តែបច្ចុប្បន្នមិនសូវមានអ្នកលក់ទឹកកកឈូសតាមដងផ្លូវ"
                    "ទៀតទេ ពីព្រោះតែទឹកកកឈូសត្រូវបានគេយកទៅកែច្នៃធ្វើជាបង្អែមជាច្រើនរសជាតិដាក់លក់នៅតាមហាងនានា។\nដោយសារតែ"
                    "ទឹកកកឈូសនេះអាចច្នៃបានច្រើនរសជាតិ យើងអាចរៀនធ្វើខ្លួនឯងហើយដាក់គ្រឿងផ្សំតាមដែលយើងចូលចិត្ត។ ចូលរួមជាមួយពួកយើងក្នុង Telegram ដើម្បីទទួលបានព័ត៌មានរហ័សគ្រឿងផ្សំ៖១. ទឹកកកដុះ២. "
                    "ស្ករត្នោតថ្មី ឬស្ករស៣. សរសៃដូងខ្ចី៤.​ ខ្ទិះដូង៥. ទឹកដោះគោខាប់៦. ទឹកសេរ៉ូ៧. ផ្លែឈើ តាមចំណូលចិត្ត៨. ឡុតឈិត គ្រាប់ជី សណ្ដែកខៀវ\nសណ្ដែកក្រហម ឆៅគួយ ដាក់តាមចំណូលចិត្ត ទឹកកកឈូសរបៀបធ្វើទឹកស្ករ៖១.​ "
                    "យកឆ្នាំងមួយសម្រាប់ដាក់ស្ករសចំនួន៣ខាំលាយជាមួយទឹក១កូនចានចង្កឹះ\nដាក់អំបិល១ចុងស្លាបព្រាបកាហ្វេចូល ហើយកូរវាឲ្យរលាយអស់ហើយ បើកភ្លើងដាំទឹកស្កររហូតដល់ពុះហើយខាប់ល្អ\nដាក់សរសៃដូងខ្ចី "
                    "ខ្ទឹះដើមចូលរួចរាល់។ ទឹកកកឈូស២. យកទឹកកកដុំនោះទៅឈូសឬយើងអាចយកទឹកកកដុំតូចៗល្អិតដែលយើងចង់បាន\nយកចានមួយដាក់គ្រឿងបង្អែម ឡុតឈិត "
                    "គ្រាប់ជី សណ្ដែកខៀវ សណ្ដែកក្រហម ផ្លែឈើផ្សេងចូលក្នុងចានហើយដាក់ទឹកកកពីលើដាក់ទឹកស្ករចូល\nចាក់ទឹកសេរ៉ូរោយ និង​ "
                    "ទឹកដោះគោខាប់ពីលើជាការស្រេច។អាហារ")
    }

    article_url = "https://lomhe.com/article/140243"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(lomhe_spider.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

