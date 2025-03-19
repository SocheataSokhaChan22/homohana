"""Test Case For SBM News Cambodia Website"""
import requests
from scrapy.http import HtmlResponse, TextResponse, Request
from url_khmer_scraping.jsonl_scraper.spiders.sbmnews import SBMSpider
import json

sbmspider = SBMSpider()

def test_parse_sbmnews():
    """
    Test the `parse` method of the SBMSpider.

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
    category_url = "https://sbm.news/categories/6626788d0168987bbf9af64a/articles"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = sbmspider.parse(category_response)

    """
    testing the parsing category 
    """
    form_request = next(category_result)
    assert form_request.meta["category_id"] == "6626788d0168987bbf9af64a"  # ទេសចរណ៏
    assert form_request.meta["page"] == 1
    assert form_request.method == "GET"


def test_parse_data_sbmnews():
    """
    Test the `parse_data` method of SBMSpider.
    
    Attributes:
    ----------
    ajax_url (str):
        The URL for the AJAX request to fetch articles.
    category_id (str):
        The ID for the news category being tested.
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
    expected_value: dict
        Expected result of the parsed data.
    """
    ajax_api = "https://sbm.news/api/articles"
    category_id = "66d1a14a37ec622bfdb644a9"
    
    form_data = {
        "page": "3",
        "categoryId": category_id,
        "locale": "km"
    }

    # Make the GET request with query parameters
    ajax_response = requests.get(ajax_api, params=form_data)
    ajax_json = ajax_response.json()

    request = Request(url=ajax_api, meta={"category_id": category_id, "page": 3})
    json_body = json.dumps(ajax_json).encode("utf-8")

    response = TextResponse(url=ajax_api, body=json_body, request=request)

    items_generator = sbmspider.parse_data(response)
    items_list = list(items_generator)

    assert len(items_list)-1 == 6

    expected_value = {
        "category": "ជាតិ, សង្គម",
        "title": "បណ្ឌិតយង់ ពៅ៖ «បើ[ខ្មែរ]ចេះច្រើនមែន ស្មើអាម៉េរិក-ស្មើអាល្លឺម៉ង់បាត់ហើយ»",
        "content": (
            "<p>រាជធានីភ្នំពេញ៖ <b>លោកបណ្ឌិត យង់ ពៅ</b> អគ្គលេខាធិការនៃរាជបណ្ឌិត្យសភាកម្ពុជា បន្តដាស់តឿនយុវជនខ្មែរ\nឱ្យប្រឹងប្រែងរៀនសូត្រ ដោយលោកថែមទាំងឆ្លៀតនិយាយរឿងនយោបាយបញ្ចូលថា <b><i>យុវជន "
            "ក៏ត្រូវរៀនពីនយោបាយដែរ\nមុនចូលធ្វើនយោបាយ</i></b>។ អ្នកជំនាញផ្នែកវិទ្យាសាស្ត្រនយោបាយរូបនេះ បានរម្លឹកសម្តីខ្លួនឯង\nដែលធ្លាប់និយាយលើកមុនៗថា អ្នកខ្លះ ត្រូវជាប់ពន្ធនាគារក្នុងរឿងនយោបាយ "
            "ព្រោះអ្នកទាំងនោះ ពុំព្រមរៀនឱ្យយល់ពីនយោបាយជាមុន។\nលោក បន្ថែមថា ព្រោះតែសម្តីនេះ លោកត្រូវគេជេរប្រមាថមិនស្ទើរឡើយ...។ </p><figure><img src=\"https://sbm.news/api/files/images/sbm-8PYac3W-o28By5V907PfW.jpg\" alt=\"លោក យង់ ពៅ "
            "ឡើងថ្លែងក្នុងវេទិកាស្តីពីទំនាក់ទំនងអន្តរជាតិលើកទី៣។\" style=\"display: block; margin: auto; max-width: 100%; width:100%\" ><figcaption style=\"text-align: center; margin-bottom: 24px\"><i>លោក "
            "យង់ ពៅ ឡើងថ្លែងក្នុងវេទិកាស្តីពីទំនាក់ទំនងអន្តរជាតិលើកទី៣។</i></figcaption></figure><p>ជាមួយគ្នានេះ លោក យង់ ពៅ "
            "បានបង្ហាញអាការដែលមើលទៅហាក់ទ្រលាន់នឹងអ្នកដែលចូលចិត្តលើកឡើងថា\nបច្ចុប្បន្ន <b>«ប្រជាជនខ្មែរចេះដឹងច្រើន»</b>។ "
            "ក្នុងនាមជាវាគ្មិនក្នុងវេទិកាស្តីពីទំនាក់ទំនងអន្តរជាតិលើកទី៣\nនៅរាជបណ្ឌិត្យសភាកម្ពុជា នាព្រឹកថ្ងៃទី៤ ខែកញ្ញា ឆ្នាំ២០២៤ "
            "បញ្ញវន្តខ្មែររូបនេះ\nបង្ហាញការយល់ឃើញផ្ទាល់ខ្លួនដូច្នេះថា៖<b>«ចេះច្រើនអី អត់ព្រមរៀន</b><b>[</b><b>ផង]</b><b>..</b><b>គេថាមិនរៀន\nថាចេះច្រើន។ បើចេះច្រើន ស្មើអាម៉េរិក ស្មើអាល្លឺម៉ង់បាត់ហើយ»</b>។ "
            "នៅមិនទាន់អស់ពាក្យទេ! លោកអគ្គលេខាធិការនៃរាជបណ្ឌិត្យសភាកម្ពុជារូបនេះ បានផ្តល់យោបល់ថា ត្រូវហ៊ានទទួលស្គាល់ពីភាពទន់ខ្សោយរបស់ខ្លួន\nដើម្បីកែប្រែខ្លួនទៅរកភាពរឹងមាំ។ ចំពោះលោក "
            "បើអ្នកណាមិនព្រមទទួលស្គាល់ថា <b>ខ្លួនទន់ខ្សោយ</b>\nអ្នកនោះនឹងនៅតែទន់ខ្សោយបន្តទៀត។ </p><figure><img src=\"https://sbm.news/api/files/images/sbm-YviiLK6yk7iHotB6SM40u.jpg\" alt=\"វាគ្មិន "
            "ស្ថិតក្នុងវេទិកាស្តីពីទំនាក់ទំនងអន្តរជាតិលើកទី៣។\" style=\"display: block; margin: auto; max-width: 100%; width:100%\" ><figcaption style=\"text-align: center; margin-bottom: 24px\"><i>វាគ្មិន ស្ថិតក្នុងវេទិកាស្តីពីទំនាក់ទំនងអន្តរជាតិលើកទី៣។</i></figcaption></figure><p>លោកបានភ្ជាប់រឿងខ្លាំងខ្សោយក្នុងបរិបទសង្គមកម្ពុជា\nទៅនឹងរឿងខ្លាំងខ្សោយក្នុងបរិបទសាកលលោក។ "
            "មន្រ្តីជាន់ខ្ពស់នៃរាជបណ្ឌិត្យសភាកម្ពុជារូបនេះ\nបានលើកពាក្យដែលខ្លួនឧស្សាហ៍និយាយថា ក្នុងពិភពលោក យុត្តិធម៌ មានសម្រាប់តែប្រទេសខ្លាំងប៉ុណ្ណោះ\nដូច្នេះ ប្រទេសទន់ខ្សោយ "
            "ត្រូវប្រឹងប្រែងរកភាពខ្លាំងឱ្យបាន។ លោក សង្កត់ធ្ងន់បែបនេះថា៖<b>«កុំទុកឱ្យពិភពលោកនេះ\nជារបស់មហាអំណាច គឺជាពិភពលោករបស់យើងដែរ»</b>៕ </p>"),
        "url": "https://sbm.news/articles/66d82eac37ec622bfdc0ec6c"
    }

    first_article = items_list[2]
    assert expected_value["category"] == first_article["category"]
    assert expected_value["title"] == first_article["title"]
    assert expected_value["content"] == first_article["content"]
    assert expected_value["url"] == first_article["url"]
