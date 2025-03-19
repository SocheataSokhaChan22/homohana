"""Test Case For Sokhakrom Cambodia Website"""
import requests
from scrapy.http import HtmlResponse, TextResponse, Request
from url_khmer_scraping.jsonl_scraper.spiders.sokhakrom import SokhakromSpider
import json

sokhakrom_pider = SokhakromSpider()
def test_parse_sokhakrom():
    """
    Test the `parse` method of SokhakromSpider.

    This test checks the initial request created by the `parse` method 
    when the spider starts crawling the category URL.

    Steps:
    ------
    - Sends a GET request to the Sokhakrom category URL.
    - Converts the response to an HtmlResponse object.
    - Invokes the spider's `parse` method and retrieves the first request.
    - Asserts the correctness of the meta data and HTTP method in the request.

    Assertions:
    -----------
    - The `page` meta value should be 1.
    - The HTTP method of the request should be GET.

    """
    category_url = "https://sokhakrom.com/kh/healthtip/list/data/all"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = sokhakrom_pider.parse(category_response)

    form_request = next(category_result)
    assert form_request.meta["page"] == 1
    assert form_request.method == "GET"


def test_parse_data_sokhakrom():
    """
    Test the `parse_data` method of SokhakromSpider.

    This test checks the article details parsed from a specific Sokhakrom article.

    Attribute
    ---------
    article_response:
        live response generated from article url
    archive_response:
        live response generated from newsroom url
    article: dict
        desired output (should be parsed)
    expected_value:
        Expected result of the parsed data.

    Steps:
    ------
    - Sends a GET request to the article URL.
    - Converts the response to an HtmlResponse object.
    - Invokes the spider's `parse_data` method with the article response and category.
    - Iterates through the article items and checks the extracted data.

    Assertions:
    -----------
    - The `category` field should not be empty.
    - The `title` field should not be empty.
    - The `content` field should not be empty.
    - The `url` field should match the article URL.

    """
    expected_value = {
        "category": "healthtip",
        "title": "តើដូចម្ដេចដែលហៅថា អាហារថ្ងៃត្រង់សុវត្ថិភាព ក្នុងអំឡុងពេលជំងឺកូរ៉ូណា (Covid-19) ? ",
        "content": ("\n                                    \n                        \n                    "
                    "\n                                តើដូចម្ដេចដែលហៅថា អាហារថ្ងៃត្រង់សុវត្ថិភាព ក្នុងអំឡុងពេលជំងឺកូរ៉ូណា "
                    "(Covid-19) ? \n                \n                \n                    ការបរិភោគអាហារថ្ងៃត្រង់ "
                    "ក្នុងអំឡុងពេលអនុវត្តន៍វិធានការ ទប់ស្កាត់ការរីករាលដាលនៃការឆ្លងជំងឺកូរ៉ូណា (Covid-19) "
                    "គឺជាកត្តាចម្បងមួយដែលយើងគ្រប់គ្នា ជាពិសេសអ្នកធ្វើការនៅតាមបណ្ដាក្រុមហ៊ុននានា គួរយកចិត្តទុកដាក់ជាទីបំផុត "
                    "ដើម្បីបន្ថយពីហានិភ័យការឆ្លងជំងឺកូរ៉ូណា (Covid-19) សម្រាប់ខ្លួនឯង មិត្តរួមការងារ គ្រួសារ និងមនុស្សនៅជុំវិញ ។ \r\n\r\nខាងក្រោមនេះជាដំបូន្មានមួយចំនួន ពាក់ព័ន្ធនឹងការបរិភោគអាហារថ្ងៃត្រង់ ក្នុងអំឡុងពេលអនុវត្តន៍វិធានការ "
                    "ទប់ស្កាត់ការរីករាលដាលនៃការឆ្លងជំងឺកូរ៉ូណា (Covid-19) ៖ \r\n\r\n១. ការបរិភោគនៅខាងក្រៅ \r\n\r\n- សង្កេតមើលទីតាំងហាងបាយ ឱ្យបានហ្មត់ចត់ ពាក់ព័ន្ធនឹងអនាម័យ ។\r\n- បង្កើតពេលវេលាឱ្យខ្លួនឯងសម្រាប់អាហារថ្ងៃត្រង់ "
                    "ឬរកម៉ោងណា ដែលពុំសូវមានមនុស្សចូលបរិភោគអាហារ (ហាងបាយមនុស្សតិច ហានិភ័យឆ្លងទាប) ។\r\n- អង្គុយបរិភោគអាហារ ដោយរក្សាគម្លាតគ្នា យ៉ាងហោចណាស់ ១ម៉ែត្រកន្លះ ។\r\n- ប្រើប្រាស់ទឹកអាល់កុល ឬជែលលាងដៃសម្លាប់មេរោគ "
                    "បាញ់ទៅលើកន្លែងអង្គុយជាមុនសិន មុននឹងចូលតុអង្គុយបរិភោគអាហារ ។\r\n- មុននឹងប្រើប្រាស់ សម ចង្កឹះ និងស្លាបព្រា សូមជ្រកលក់ទៅក្នុងទឹកក្ដៅសិនសម្លាប់មេរោគសិន ឬបើហាងបាយគ្មានទឹកក្ដៅ អាចស្នើសុំម្ចាស់ហាងសុំទឹកក្ដៅមួយកែវ ។\r\n\r\n២. ការបរិភោគនៅខាងក្នុង \r\n\r\nក្នុងបរិបទទប់ស្កាត់ការរីករាលដាលនៃជំងឺកូរ៉ូណា (Covid-19) "
                    "គឺសូមរៀបចំចម្អិនចំណីអាហារពីផ្ទះ មកបរិភោគនៅកន្លែងការងារ ចៀសវាងការចេញបរិភោគអាហារនៅខាងក្រៅ ឬអាចកម្មង់អាហារ តាមរយៈកម្មវិធីដឹកជញ្ជូនអាហារផ្សេងៗ ។\r\n\r\nប្រសើរបំផុត ពេលចេញពីធ្វើការក្នុងម៉ោងសម្រាកអាហារថ្ងៃត្រង់ "
                    "អាចធ្វើដំណើរទៅបរិភោគអាហារនៅគេហដ្ឋានរបស់លោកអ្នក ។ តែយ៉ាងណាមិញ សូមអនុវត្តន៍អនាម័យឱ្យបានត្រឹមត្រូវជានិច្ច ៕  \r\n\r\nស្រាវជ្រាវ រៀបរៀង និងកែសម្រួលអត្ថបទដោយ ក្រុមការងារ "
                    "សុខក្រម-Sokhakrom \r\n\r\nសុខក្រម-Sokhakrom កម្មវិធីសុខភាពនៅលើទូរស័ព្ទដៃ ទាញយកដោយសេរី ដើម្បីអានអត្ថបទ និងទស្សនាវីដេអូសុខភាព បកស្រាយដោយ វេជ្ជបណ្ឌិតល្បីៗក្នុងប្រទេសកម្ពុជា ។ \r\nសូមគោរពជូន វេជ្ជបណ្ឌិត "
                    "ដែលចង់ចែករំលែកគន្លឹះសុខភាព សូមទំនាក់ទំនងមកកាន់ក្រុមការងារ សុខក្រម-Sokhakrom យើងខ្ញុំ តាមរយៈទំព័រហ្វេសបុក sokhakrom និងវេបសាយ sokhakrom.com ។\r\n \n                \n                            "),
    }

    article_url = "https://sokhakrom.com/kh/healthtip/detail/1319"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")
    category = "healthtip"
    article = next(sokhakrom_pider.parse_data(article_response, category))

    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url


def test_parse_data_ajax_sokhakrom():
    """
    Test the `parse_data_ajax` method of SokhakromSpider.

    This test simulates an AJAX request to load articles via the "Load More" functionality.

    Steps:
    ------
    - Sends a GET request to the category URL with query parameters.
    - Converts the response to a JSON object.
    - Creates a request object with the meta data for the AJAX response.
    - Converts the JSON data to a TextResponse object for parsing.
    - Invokes the spider's `parse_data_ajax` method and retrieves the items.
    - Asserts the number of items returned and checks the URL of the last item.

    Assertions:
    -----------
    - The total number of items returned should be 7.
    - The URL of the last item should match the expected AJAX URL.

    """
    category_url = "https://sokhakrom.com/kh/healthtip/list/data/all"
    form_data = {
        "page": "2",
        "search": "",
        "sort": "nto"
    }

    # Make the GET request with query parameters
    ajax_response = requests.get(category_url, params=form_data)
    ajax_json = ajax_response.json()

    request = Request(url=category_url, meta={"page": 1})
    json_body = json.dumps(ajax_json).encode("utf-8")

    response = TextResponse(url=category_url, body=json_body, request=request)

    items_generator = sokhakrom_pider.parse_data_ajax(response)
    items_list = list(items_generator)

    assert len(items_list) == 7
    assert items_list[6].url == 'https://sokhakrom.com/kh/healthtip/list/data/all?page=2&search=&sort=nto'
